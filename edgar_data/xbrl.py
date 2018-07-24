# Credits:
# This module uses Open Source components. You can find the source code
# for the full project in the url below:
# https://github.com/lukerosiak/pysec
#
# The GAAP and IFRS data are changed to be None if missing, instead of 0

import re
from collections import defaultdict
from datetime import datetime

from lxml import etree
from lxml.etree import XPathEvalError, XMLParser

from edgar_data.currency import find_currency
from .xbrl_fundamentals import FundamentantalAccountingConcepts


class EDGARPeriodError(Exception):
    """A period could not be found."""


class FieldSegmentError(Exception):
    """Could not find segment results for the given field."""


class Field:
    def __init__(self, value, unit_ref, xbrl=None, concept=None):
        self.value = value
        self.unit_ref = unit_ref
        self.xbrl = xbrl
        self.concept = concept

    @property
    def currency(self):
        if self.unit_ref is not None:
            return find_currency(self.unit_ref)
        else:
            return None

    @property
    def segment_values(self):
        if self.xbrl is None or self.concept is None:
            raise FieldSegmentError("Can't find segment values for the given concept (probably was calculated).")
        else:
            return list(self.xbrl.get_segment_values(self.concept))

    def __add__(self, other):
        return Field(self.value + other.value, self.unit_ref)

    def __sub__(self, other):
        return Field(self.value - other.value, self.unit_ref)

    def __float__(self):
        return float(self.value)

    def __str__(self):
        return str(self.value)


class FieldsDataset:

    def __init__(self):
        self.fields = {}

    def __getitem__(self, item):
        try:
            field = self.fields[item]
        except KeyError:
            return None

        return field

    def __setitem__(self, key, value):
        self.fields[key] = value

    def currency(self, key):
        if isinstance(self[key], Field):
            return self.fields[key].currency
        else:
            return None


class XBRL:

    fact_labels = {
        'Revenues':
            [
                "us-gaap:Revenues",
                "us-gaap:SalesRevenueNet",
                "us-gaap:SalesRevenueServicesNet",
                "us-gaap:RevenuesNetOfInterestExpense",
                "us-gaap:RegulatedAndUnregulatedOperatingRevenue",
                "us-gaap:HealthCareOrganizationRevenue",
                "us-gaap:InterestAndDividendIncomeOperating",
                "us-gaap:RealEstateRevenueNet",
                "us-gaap:RevenueMineralSales",
                "us-gaap:OilAndGasRevenue",
                "us-gaap:FinancialServicesRevenue",
                "us-gaap:RegulatedAndUnregulatedOperatingRevenue",
                "ifrs-full:Revenue",
                "ifrs-full:RevenueFromSaleOfOilAndGasProducts"
            ],
        'NetIncomeAttributableToParent':
            [
                "us-gaap:NetIncomeLoss",
                "ifrs-full:ProfitLossAttributableToOwnersOfParent"
            ],
        'NetIncomeLoss':
            [
                "us-gaap:ProfitLoss",
                "us-gaap:NetIncomeLoss",
                "us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic",
                "us-gaap:IncomeLossFromContinuingOperations",
                "us-gaap:IncomeLossAttributableToParent",
                "us-gaap:IncomeLossFromContinuingOperationsIncludingPortionAttributableToNoncontrollingInterest"
            ]
    }

    def __init__(self, xbrl_doc):

        self.fields = FieldsDataset()

        self.EntireInstanceDocument = xbrl_doc
        p = XMLParser(huge_tree=True)
        self.oInstance = etree.fromstring(self.EntireInstanceDocument, parser=p)
        self.ns = {}
        for k in list(self.oInstance.nsmap.keys()):
            if k != None:
                self.ns[k] = self.oInstance.nsmap[k]
        self.ns['xbrli'] = 'http://www.xbrl.org/2003/instance'
        self.ns['xlmns'] = 'http://www.xbrl.org/2003/instance'

        self.GetBaseInformation()
        self.loadYear(0)

    def loadYear(self, yearminus=0, quarter=False):
        currentEnd = self.getNode("//dei:DocumentPeriodEndDate").text
        asdate = re.match('\s*(\d{4})-(\d{2})-(\d{2})\s*', currentEnd)
        if asdate:
            year = int(asdate.groups()[0]) - yearminus
            thisend = '%s-%s-%s' % (year, asdate.groups()[1], asdate.groups()[2])
            self.GetCurrentPeriodAndContextInformation(thisend, quarter)
            FundamentantalAccountingConcepts(self)
            return True
        else:
            #print(currentEnd, ' is not a date')
            return False

    def getNodeList(self, xpath, root=None):
        if not root is not None: root = self.oInstance
        try:
            oNodelist = root.xpath(xpath, namespaces=self.ns)
        except XPathEvalError:
            return []
        return oNodelist

    def getNode(self, xpath, root=None):
        oNodelist = self.getNodeList(xpath, root)
        if len(oNodelist):
            return oNodelist[0]
        return None

    def get_fact_value(self, concept, period_type):
        fact_value = None
        for fact_name in self.fact_labels[concept]:
            fact_value = self.GetFactValue(fact_name, period_type)
            if fact_value is not None:
                break

        if fact_value is not None:
            fact_value.concept = concept

        return fact_value

    def GetFactValue(self, SeekConcept, ConceptPeriodType):

        factValue = None
        field = None

        if ConceptPeriodType == "Instant":
            ContextReference = self.fields['ContextForInstants']
        elif ConceptPeriodType == "Duration":
            ContextReference = self.fields['ContextForDurations']
        else:
            # An error occured
            return "CONTEXT ERROR"

        if not ContextReference:
            return None

        oNode = self.getNode("//" + SeekConcept + "[@contextRef='" + ContextReference + "']")
        if oNode is not None:
            factValue = oNode.text
            if 'nil' in list(oNode.keys()) and oNode.get('nil') == 'true':
                factValue = 0
                # set the value to ZERO if it is nil
            # if type(factValue)==str:
            try:
                factValue = float(factValue)
            except:
                #print('couldnt convert %s=%s to string' % (SeekConcept, factValue))
                factValue = None
                pass

        if factValue is not None:
            unit = self.getNode("//xbrli:unit[@id='" + oNode.attrib['unitRef'] + "']//xbrli:measure")
            if unit is not None:
                field = Field(value=factValue, unit_ref=unit.text, xbrl=self)
            else:
                field = Field(value=factValue, unit_ref=None, xbrl=self)

        return field

    def GetBaseInformation(self):

        # Registered Name
        oNode = self.getNode("//dei:EntityRegistrantName[@contextRef]")
        if oNode is not None:
            self.fields['EntityRegistrantName'] = oNode.text
        else:
            self.fields['EntityRegistrantName'] = None

        # Fiscal year
        oNode = self.getNode("//dei:CurrentFiscalYearEndDate[@contextRef]")
        if oNode is not None:
            self.fields['FiscalYear'] = oNode.text
        else:
            self.fields['FiscalYear'] = None

        # EntityCentralIndexKey
        oNode = self.getNode("//dei:EntityCentralIndexKey[@contextRef]")
        if oNode is not None:
            self.fields['EntityCentralIndexKey'] = oNode.text
        else:
            self.fields['EntityCentralIndexKey'] = None

        # EntityFilerCategory
        oNode = self.getNode("//dei:EntityFilerCategory[@contextRef]")
        if oNode is not None:
            self.fields['EntityFilerCategory'] = oNode.text
        else:
            self.fields['EntityFilerCategory'] = None

        # TradingSymbol
        oNode = self.getNode("//dei:TradingSymbol[@contextRef]")
        if oNode is not None:
            self.fields['TradingSymbol'] = oNode.text
        else:
            self.fields['TradingSymbol'] = None

        # DocumentFiscalYearFocus
        oNode = self.getNode("//dei:DocumentFiscalYearFocus[@contextRef]")
        if oNode is not None:
            self.fields['DocumentFiscalYearFocus'] = oNode.text
        else:
            self.fields['DocumentFiscalYearFocus'] = None

        # DocumentFiscalPeriodFocus
        oNode = self.getNode("//dei:DocumentFiscalPeriodFocus[@contextRef]")
        if oNode is not None:
            self.fields['DocumentFiscalPeriodFocus'] = oNode.text
        else:
            self.fields['DocumentFiscalPeriodFocus'] = None

        # DocumentType
        oNode = self.getNode("//dei:DocumentType[@contextRef]")
        if oNode is not None:
            self.fields['DocumentType'] = oNode.text
        else:
            self.fields['DocumentType'] = None

    def GetCurrentPeriodAndContextInformation(self, EndDate, quarter=False):
        # Figures out the current period and contexts for the current period instance/duration contexts

        self.fields['BalanceSheetDate'] = "ERROR"
        self.fields['IncomeStatementPeriodYTD'] = "ERROR"

        self.fields['ContextForInstants'] = "ERROR"
        self.fields['ContextForDurations'] = "ERROR"

        # This finds the period end date for the database table, and instant date (for balance sheet):
        UseContext = "ERROR"
        # EndDate = self.getNode("//dei:DocumentPeriodEndDate").text
        # This is the <instant> or the <endDate>

        # Uses the concept ASSETS to find the correct instance context
        # This finds the Context ID for that end date (has correct <instant> date plus has no dimensions):
        oNodelist2 = self.getNodeList(
            "//us-gaap:Assets | //us-gaap:AssetsCurrent | //us-gaap:LiabilitiesAndStockholdersEquity")
        # Nodelist of all the facts which are us-gaap:Assets
        for i in oNodelist2:
            # #print i.XML

            ContextID = i.get('contextRef')
            ContextPeriod = self.getNode("//xbrli:context[@id='" + ContextID + "']/xbrli:period/xbrli:instant").text
            #print(ContextPeriod)

            # Nodelist of all the contexts of the fact us-gaap:Assets
            oNodelist3 = self.getNodeList("//xbrli:context[@id='" + ContextID + "']")
            for j in oNodelist3:

                # Nodes with the right period
                if self.getNode("xbrli:period/xbrli:instant", j) is not None and self.getNode(
                        "xbrli:period/xbrli:instant", j).text == EndDate:

                    oNode4 = self.getNodeList("xbrli:entity/xbrli:segment/xbrldi:explicitMember", j)

                    if not len(oNode4):
                        UseContext = ContextID
                        #print(UseContext)


        #NOTE: if the DocumentPeriodEndDate is incorrect, this attempts to fix it by looking for a few commonly occuring concepts for the current period...
        if UseContext=="ERROR":
            #print 'if the DocumentPeriodEndDate is incorrect, this attempts to fix it by looking for a few commonly occuring concepts for the current period...'                    
            oNodelist_Error = self.getNode("//dei:DocumentPeriodEndDate")
            if oNodelist_Error is None:
                oNodelist_Error = self.getNode("//us-gaap:OrganizationConsolidationAndPresentationOfFinancialStatementsDisclosureTextBlock | //us-gaap:SignificantAccountingPoliciesTextBlock")
            ##print "Nodelist, trying to find alternative: " + oNodelist_Error.length
            
            ContextID = oNodelist_Error.get('contextRef')
            ContextPeriod = self.getNode("//xbrli:context[@id='" + ContextID + "']/xbrli:period/xbrli:endDate").text

            #print "Found Alternative: " + ContextPeriod
            
            oNodelist3 = self.getNodeList("//xbrli:context[xbrli:period/xbrli:instant='" + ContextPeriod + "']")
            ##print "Found alternative contexts:" + oNodelist3.length
            
            for j in oNodelist3:
                ##print j.XML
                
                #Nodes with the right period
                if self.getNode("xbrli:period/xbrli:instant",j).text==ContextPeriod:
                    oNode4 = self.getNodeList("xbrli:entity/xbrli:segment/xbrldi:explicitMember",j)
                    ##print "Found dimension: " + oNode4.XML
                    #WHATS GOING ON HERE                
                    
                    if len(oNode4):
                        #Not the right context
                        #print "Note4: " + oNode4[0].text
                        pass
                    else:
                        ##print "SELECTED CONTEXT: " + oNodelist3.Item(j).selectSingleNode("./@id").text 'oNodelist3(j).XML
                        ContextID = j.get("id")
                        UseContext = ContextID
                        ##print UseContext
                                        
                    ##print j.XML
                                    
            #EndDate = ContextPeriod

        ContextForInstants = UseContext
        self.fields['ContextForInstants'] = ContextForInstants

        ###This finds the duration context
        ###This may work incorrectly for fiscal year ends because the dates cross calendar years
        # Get context ID of durations and the start date for the database table

        StartDate = "ERROR"
        StartDateYTD = "2099-01-01"
        UseContext = "ERROR"
        date_format = "%Y-%m-%d"
        end = datetime.strptime(EndDate, date_format)

        # Based on https://xbrl.us/data-rule/dqc_0006pr/
        if quarter:
            ndays = 90
            days_tol_upper = 119 - ndays
            days_tol_lower = ndays - 77
        else:
            period = self.fields['DocumentFiscalPeriodFocus']

            if period == 'FY':
                ndays = 364
                days_tol_upper = 379 - ndays
                days_tol_lower = ndays - 350
            elif period == 'Q1':
                ndays = 90*1
                days_tol_upper = 119 - ndays
                days_tol_lower = ndays - 77
            elif period == 'Q2':
                ndays = 90*2
                days_tol_upper = 204 - ndays
                days_tol_lower = ndays - 154
            elif period == 'Q3':
                ndays = 90*3
                days_tol_upper = 287 - ndays
                days_tol_lower = ndays - 238
            else:
                raise ValueError("Unknown fiscal period focus.")

        all_contexts = self.getNodeList("//xbrli:context")

        for context in all_contexts:
            context_end_date = self.getNode("xbrli:period/xbrli:endDate", context)
            # Nodes with the right period
            if context_end_date is not None and context_end_date.text == EndDate:

                has_dimensions = self.getNodeList("xbrli:entity/xbrli:segment/xbrldi:explicitMember", context)
                if not len(has_dimensions):
                    StartDate = self.getNode("xbrli:period/xbrli:startDate", context).text
                    start = datetime.strptime(StartDate, date_format)
                    old_start = datetime.strptime(StartDateYTD, date_format)

                    delta = abs(end - start).days
                    old_delta = abs(end - old_start).days

                    if abs(delta - ndays) < abs(old_delta - ndays):
                        StartDateYTD = StartDate
                        UseContext = context.get('id')

        start = datetime.strptime(StartDateYTD, date_format)
        end = datetime.strptime(EndDate, date_format)
        delta = abs(end - start).days

        if abs(delta) < (ndays-days_tol_lower) or abs(delta) > (ndays+days_tol_upper):
            raise EDGARPeriodError("Could not find a valid period. "
                                   "Found delta={0} but needed {1}".format(delta, ndays))

        if StartDate == "ERROR" or StartDateYTD == "2099-01-01" or UseContext == "ERROR":
            raise EDGARPeriodError("Could not find a valid context.")

        # Balance sheet date of current period
        self.fields['BalanceSheetDate'] = EndDate

        # MsgBox "Instant context is: " + ContextForInstants
        if ContextForInstants == "ERROR":
            # MsgBox "Looking for alternative instance context"

            ContextForInstants = self.LookForAlternativeInstanceContext()
            self.fields['ContextForInstants'] = ContextForInstants

        # Income statement date for current fiscal year, year to date
        self.fields['IncomeStatementPeriodYTD'] = StartDateYTD

        ContextForDurations = UseContext
        self.fields['ContextForDurations'] = ContextForDurations

        self.fields['ContextForBusinessSegments'] = []

        all_contexts = self.getNodeList("//xbrli:context")

        for context in all_contexts:
            context_start_date = self.getNode("xbrli:period/xbrli:startDate", context)
            context_end_date = self.getNode("xbrli:period/xbrli:endDate", context)
            # Nodes with the right period
            if context_end_date is not None and context_start_date is not None \
                    and context_start_date.text == StartDateYTD and context_end_date.text == EndDate:
                business_segments = self.getNodeList("xbrli:entity/xbrli:segment/xbrldi:explicitMember[@dimension='us-gaap:StatementBusinessSegmentsAxis']", context)
                if business_segments:
                    self.fields['ContextForBusinessSegments'].append((context, business_segments[0].text))

    def _get_context_dims(self, context):
        return self.getNodeList(
            "xbrli:entity/xbrli:segment/xbrldi:explicitMember[@dimension!='us-gaap:StatementBusinessSegmentsAxis']",
            context)

    def get_segment_values(self, concept):
        segments = defaultdict(list)
        for segment_context, segment_name in self.fields['ContextForBusinessSegments']:
            # print(concept, segment_context.get('id'))

            for fact_name in self.fact_labels[concept]:
                oNode = self.getNode("//" + fact_name + "[@contextRef='" + segment_context.get('id') + "']")
                if oNode is not None:
                    segments[segment_name].append({"dims": self._get_context_dims(segment_context), "node": oNode})

        #print(self.fields['ContextForBusinessSegments'])

        for segment_name, contexts in segments.items():
            # print("Before")
            # print(len(contexts))
            # for context in contexts:
            #     print('->', context["node"].get('contextRef'))
            #     for dim in context["dims"]:
            #         print('  ', dim.get('dimension'))
            #         print('      ', dim.text)

            if len(contexts) > 1:
                contexts = [context
                            for context in contexts
                            if all(dim.get('dimension') != 'us-gaap:StatementScenarioAxis'
                                   for dim in context["dims"])]

            # print(len(contexts))
            # for context in contexts:
            #     print('->', context["node"].get('contextRef'))
            #     for dim in context["dims"]:
            #         print('  ', dim.get('dimension'))
            #         print('      ', dim.text)

            if len(contexts) > 1:
                contexts = [context
                            for context in contexts
                            if not any((dim.get('dimension') == 'us-gaap:ConsolidationItemsAxis'
                                        and 'elimination' in dim.text.lower())
                                       for dim in context["dims"])]

            if len(contexts) > 1:
                contexts = [context
                            for context in contexts
                            if any(dim.text == 'us-gaap:OperatingSegmentsMember'
                                   for dim in context["dims"])]

            # print("After")
            # print(len(contexts))
            # for context in contexts:
            #     print('->', context["node"].get('contextRef'))
            #     print('value:', float(context["node"].text))
            #     for dim in context["dims"]:
            #         print('  ', dim.get('dimension'))
            #         print('      ', dim.text)

            if len(contexts) > 1:
                raise FieldSegmentError("Could not eliminate enough segments.")
            # input('')

            if contexts:
                yield (segment_name, float(contexts[0]["node"].text))

    def LookForAlternativeInstanceContext(self):
        # This deals with the situation where no instance context has no dimensions
        # Finds something

        something = None

        # See if there are any nodes with the document period focus date
        oNodeList_Alt = self.getNodeList(
            "//xbrli:context[xbrli:period/xbrli:instant='" + self.fields['BalanceSheetDate'] + "']")

        # MsgBox "Node list length: " + oNodeList_Alt.length
        for oNode_Alt in oNodeList_Alt:
            # Found possible contexts
            # MsgBox oNode_Alt.selectSingleNode("@id").text
            something = self.getNode("//us-gaap:Assets[@contextRef='" + oNode_Alt.get("id") + "']")
            if something:
                # MsgBox "Use this context: " + oNode_Alt.selectSingleNode("@id").text
                return oNode_Alt.get("id")
