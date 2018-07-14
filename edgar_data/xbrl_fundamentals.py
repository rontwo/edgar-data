# Credits:
# This module uses Open Source components. You can find the source code
# for the full project in the url below:
# https://github.com/lukerosiak/pysec

class FundamentantalAccountingConcepts:

    def __init__(self, xbrl, no_output=True):

        self.xbrl = xbrl

        if not no_output:
            print(" ")
            print("FUNDAMENTAL ACCOUNTING CONCEPTS CHECK REPORT:")

            print("Entity regiant name: %s" % self.xbrl.fields['EntityRegistrantName'])
            print("CIK: %s" % self.xbrl.fields['EntityCentralIndexKey'])
            print("Entity filer category: %s" % self.xbrl.fields['EntityFilerCategory'])
            print("Trading symbol: %s" % self.xbrl.fields['TradingSymbol'])
            print("Fiscal year: %s" % self.xbrl.fields['DocumentFiscalYearFocus'])
            print("Fiscal period: %s" % self.xbrl.fields['DocumentFiscalPeriodFocus'])
            print("Document type: %s" % self.xbrl.fields['DocumentType'])

            print("Balance Sheet Date (document period end date): %s" % self.xbrl.fields['BalanceSheetDate'])
            print("Income Statement Period (YTD, current period, period start date): %s to %s" % (
                self.xbrl.fields['IncomeStatementPeriodYTD'], self.xbrl.fields['BalanceSheetDate']))

            print("Context ID for document period focus (instants): %s" % self.xbrl.fields['ContextForInstants'])
            print("Context ID for YTD period (durations): %s" % self.xbrl.fields['ContextForDurations'])
            print(" ")

        # Assets
        self.xbrl.fields['Assets'] = self.xbrl.GetFactValue("us-gaap:Assets", "Instant")

        # Current Assets
        self.xbrl.fields['CurrentAssets'] = self.xbrl.GetFactValue("us-gaap:AssetsCurrent", "Instant")

        # Noncurrent Assets
        self.xbrl.fields['NoncurrentAssets'] = self.xbrl.GetFactValue("us-gaap:AssetsNoncurrent", "Instant")
        if self.xbrl.fields['NoncurrentAssets'] is None:
            if self.xbrl.fields['Assets'] and self.xbrl.fields['CurrentAssets']:
                self.xbrl.fields['NoncurrentAssets'] = self.xbrl.fields['Assets'] - self.xbrl.fields['CurrentAssets']

        # LiabilitiesAndEquity
        self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue("us-gaap:LiabilitiesAndStockholdersEquity",
                                                                          "Instant")
        if self.xbrl.fields['LiabilitiesAndEquity'] is None:
            self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue("us-gaap:LiabilitiesAndPartnersCapital",
                                                                              "Instant")

        # Liabilities
        self.xbrl.fields['Liabilities'] = self.xbrl.GetFactValue("us-gaap:Liabilities", "Instant")

        # CurrentLiabilities
        self.xbrl.fields['CurrentLiabilities'] = self.xbrl.GetFactValue("us-gaap:LiabilitiesCurrent", "Instant")

        # Noncurrent Liabilities
        self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.GetFactValue("us-gaap:LiabilitiesNoncurrent", "Instant")
        if self.xbrl.fields['NoncurrentLiabilities'] is None:
            if self.xbrl.fields['Liabilities'] and self.xbrl.fields['CurrentLiabilities']:
                self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.fields['Liabilities'] - self.xbrl.fields[
                    'CurrentLiabilities']

        # CommitmentsAndContingencies
        self.xbrl.fields['CommitmentsAndContingencies'] = self.xbrl.GetFactValue("us-gaap:CommitmentsAndContingencies",
                                                                                 "Instant")

        # TemporaryEquity
        self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("us-gaap:TemporaryEquityRedemptionValue",
                                                                     "Instant")
        if self.xbrl.fields['TemporaryEquity'] is None:
            self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue(
                "us-gaap:RedeemablePreferredStockCarryingAmount", "Instant")
            if self.xbrl.fields['TemporaryEquity'] is None:
                self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("us-gaap:TemporaryEquityCarryingAmount",
                                                                             "Instant")
                if self.xbrl.fields['TemporaryEquity'] is None:
                    self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue(
                        "us-gaap:TemporaryEquityValueExcludingAdditionalPaidInCapital", "Instant")
                    if self.xbrl.fields['TemporaryEquity'] is None:
                        self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue(
                            "us-gaap:TemporaryEquityCarryingAmountAttributableToParent", "Instant")
                        if self.xbrl.fields['TemporaryEquity'] is None:
                            self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue(
                                "us-gaap:RedeemableNoncontrollingInterestEquityFairValue", "Instant")

        RedeemableNoncontrollingInterest = self.xbrl.GetFactValue(
            "us-gaap:RedeemableNoncontrollingInterestEquityCarryingAmount", "Instant")
        if RedeemableNoncontrollingInterest == None:
            RedeemableNoncontrollingInterest = self.xbrl.GetFactValue(
                "us-gaap:RedeemableNoncontrollingInterestEquityCommonCarryingAmount", "Instant")

        # This adds redeemable noncontrolling interest and temporary equity which are rare, but can be reported seperately
        if self.xbrl.fields['TemporaryEquity'] and RedeemableNoncontrollingInterest:
            self.xbrl.fields['TemporaryEquity'] = float(self.xbrl.fields['TemporaryEquity']) + float(
                RedeemableNoncontrollingInterest)

        # Equity
        self.xbrl.fields['Equity'] = self.xbrl.GetFactValue(
            "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest", "Instant")
        if self.xbrl.fields['Equity'] is None:
            self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("us-gaap:StockholdersEquity", "Instant")
            if self.xbrl.fields['Equity'] is None:
                self.xbrl.fields['Equity'] = self.xbrl.GetFactValue(
                    "us-gaap:PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest", "Instant")
                if self.xbrl.fields['Equity'] is None:
                    self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("us-gaap:PartnersCapital", "Instant")
                    if self.xbrl.fields['Equity'] is None:
                        self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("us-gaap:CommonStockholdersEquity",
                                                                            "Instant")
                        if self.xbrl.fields['Equity'] is None:
                            self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("us-gaap:MemberEquity", "Instant")
                            if self.xbrl.fields['Equity'] is None:
                                self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("us-gaap:AssetsNet", "Instant")

        # EquityAttributableToNoncontrollingInterest
        self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue(
            "us-gaap:MinorityInterest", "Instant")
        if self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] is None:
            self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue(
                "us-gaap:PartnersCapitalAttributableToNoncontrollingInterest", "Instant")

        # EquityAttributableToParent
        self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.GetFactValue("us-gaap:StockholdersEquity", "Instant")
        if self.xbrl.fields['EquityAttributableToParent'] is None:
            self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.GetFactValue(
                "us-gaap:LiabilitiesAndPartnersCapital", "Instant")

        # Added to fix Assets
        if self.xbrl.fields['Assets'] is None \
                and self.xbrl.fields['LiabilitiesAndEquity'] is not None \
                and self.xbrl.fields['CurrentAssets'] == self.xbrl.fields['LiabilitiesAndEquity']:
            self.xbrl.fields['Assets'] = self.xbrl.fields['CurrentAssets']

        # Added to fix Assets even more
        if self.xbrl.fields['Assets'] is None \
                and self.xbrl.fields['NoncurrentAssets'] is None \
                and self.xbrl.fields['LiabilitiesAndEquity'] is not None \
                and self.xbrl.fields['Liabilities'] is not None \
                and self.xbrl.fields['Equity'] is not None \
                and (self.xbrl.fields['LiabilitiesAndEquity'] == self.xbrl.fields['Liabilities'] + self.xbrl.fields[
            'Equity']):
            self.xbrl.fields['Assets'] = self.xbrl.fields['CurrentAssets']

        if self.xbrl.fields['Assets'] is not None and self.xbrl.fields['CurrentAssets'] is not None:
            self.xbrl.fields['NoncurrentAssets'] = self.xbrl.fields['Assets'] - self.xbrl.fields['CurrentAssets']

        if self.xbrl.fields['LiabilitiesAndEquity'] is None and self.xbrl.fields['Assets'] is not None:
            self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.fields['Assets']

        # Impute: Equity based no parent and noncontrolling interest being present
        if self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] is not None \
                and self.xbrl.fields['EquityAttributableToParent'] is not None:
            self.xbrl.fields['Equity'] = self.xbrl.fields['EquityAttributableToParent'] + self.xbrl.fields[
                'EquityAttributableToNoncontrollingInterest']

        if self.xbrl.fields['Equity'] is None \
                and self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] is None \
                and self.xbrl.fields['EquityAttributableToParent'] is not None:
            self.xbrl.fields['Equity'] = self.xbrl.fields['EquityAttributableToParent']

        if self.xbrl.fields['Equity'] is None \
                and self.xbrl.fields['EquityAttributableToParent'] is not None \
                and self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] is not None:
            self.xbrl.fields['Equity'] = self.xbrl.fields['EquityAttributableToParent'] + \
                                         self.xbrl.fields['EquityAttributableToNoncontrollingInterest']

        # Added: Impute Equity attributable to parent based on existence of equity and noncontrolling interest.
        if self.xbrl.fields['Equity'] is not None \
                and self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] is not None \
                and self.xbrl.fields['EquityAttributableToParent'] is None:
            self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.fields['Equity'] - \
                                                             self.xbrl.fields[
                                                                 'EquityAttributableToNoncontrollingInterest']

        # Added: Impute Equity attributable to parent based on existence of equity and noncontrolling interest.
        if self.xbrl.fields['Equity'] is not None \
                and self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] is None \
                and self.xbrl.fields['EquityAttributableToParent'] is None:
            self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.fields['Equity']

        # if total liabilities is missing, figure it out based on liabilities and equity
        if self.xbrl.fields['Liabilities'] is None \
                and self.xbrl.fields['Equity'] is not None \
                and self.xbrl.fields['LiabilitiesAndEquity'] is not None \
                and self.xbrl.fields['CommitmentsAndContingencies'] is not None \
                and self.xbrl.fields['TemporaryEquity'] is not None:
            self.xbrl.fields['Liabilities'] = self.xbrl.fields['LiabilitiesAndEquity'] - (
                    self.xbrl.fields['CommitmentsAndContingencies'] + self.xbrl.fields['TemporaryEquity'] +
                    self.xbrl.fields['Equity'])

        # This seems incorrect because liabilities might not be reported
        if self.xbrl.fields['Liabilities'] is not None and self.xbrl.fields['CurrentLiabilities'] is not None:
            self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.fields['Liabilities'] - \
                                                        self.xbrl.fields['CurrentLiabilities']
        # Added to fix liabilities based on current liabilities
        if self.xbrl.fields['Liabilities'] is None \
                and self.xbrl.fields['CurrentLiabilities'] is not None \
                and self.xbrl.fields['NoncurrentLiabilities'] is None:
            self.xbrl.fields['Liabilities'] = self.xbrl.fields['CurrentLiabilities']

        # Income statement
        # Revenues
        self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue("us-gaap:Revenues", "Duration")
        if self.xbrl.fields['Revenues'] is None:
            self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue("us-gaap:SalesRevenueNet", "Duration")
            if self.xbrl.fields['Revenues'] is None:
                self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue("us-gaap:SalesRevenueServicesNet", "Duration")
                if self.xbrl.fields['Revenues'] is None:
                    self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue("us-gaap:RevenuesNetOfInterestExpense",
                                                                          "Duration")
                    if self.xbrl.fields['Revenues'] is None:
                        self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue(
                            "us-gaap:RegulatedAndUnregulatedOperatingRevenue", "Duration")
                        if self.xbrl.fields['Revenues'] is None:
                            self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue(
                                "us-gaap:HealthCareOrganizationRevenue", "Duration")
                            if self.xbrl.fields['Revenues'] is None:
                                self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue(
                                    "us-gaap:InterestAndDividendIncomeOperating", "Duration")
                                if self.xbrl.fields['Revenues'] is None:
                                    self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue(
                                        "us-gaap:RealEstateRevenueNet", "Duration")
                                    if self.xbrl.fields['Revenues'] is None:
                                        self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue(
                                            "us-gaap:RevenueMineralSales", "Duration")
                                        if self.xbrl.fields['Revenues'] is None:
                                            self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue(
                                                "us-gaap:OilAndGasRevenue", "Duration")
                                            if self.xbrl.fields['Revenues'] is None:
                                                self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue(
                                                    "us-gaap:FinancialServicesRevenue", "Duration")
                                                if self.xbrl.fields['Revenues'] is None:
                                                    self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue(
                                                        "us-gaap:RegulatedAndUnregulatedOperatingRevenue", "Duration")

        # CostOfRevenue
        self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("us-gaap:CostOfRevenue", "Duration")
        if self.xbrl.fields['CostOfRevenue'] is None:
            self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("us-gaap:CostOfServices", "Duration")
            if self.xbrl.fields['CostOfRevenue'] is None:
                self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("us-gaap:CostOfGoodsSold", "Duration")
                if self.xbrl.fields['CostOfRevenue'] is None:
                    self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("us-gaap:CostOfGoodsAndServicesSold",
                                                                               "Duration")

        # GrossProfit
        self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue("us-gaap:GrossProfit", "Duration")
        if self.xbrl.fields['GrossProfit'] is None:
            self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue("us-gaap:GrossProfit", "Duration")

        # OperatingExpenses
        self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue("us-gaap:OperatingExpenses", "Duration")
        if self.xbrl.fields['OperatingExpenses'] is None:
            self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue("us-gaap:OperatingCostsAndExpenses",
                                                                           "Duration")  # This concept seems incorrect.

        # CostsAndExpenses
        self.xbrl.fields['CostsAndExpenses'] = self.xbrl.GetFactValue("us-gaap:CostsAndExpenses", "Duration")
        if self.xbrl.fields['CostsAndExpenses'] is None:
            self.xbrl.fields['CostsAndExpenses'] = self.xbrl.GetFactValue("us-gaap:CostsAndExpenses", "Duration")

        # OtherOperatingIncome
        self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.GetFactValue("us-gaap:OtherOperatingIncome", "Duration")
        if self.xbrl.fields['OtherOperatingIncome'] is None:
            self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.GetFactValue("us-gaap:OtherOperatingIncome",
                                                                              "Duration")

        # OperatingIncomeLoss
        self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue("us-gaap:OperatingIncomeLoss", "Duration")
        if self.xbrl.fields['OperatingIncomeLoss'] is None:
            self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue("us-gaap:OperatingIncomeLoss", "Duration")

        # NonoperatingIncomeLoss
        self.xbrl.fields['NonoperatingIncomeLoss'] = self.xbrl.GetFactValue("us-gaap:NonoperatingIncomeExpense",
                                                                            "Duration")
        if self.xbrl.fields['NonoperatingIncomeLoss'] is None:
            self.xbrl.fields['NonoperatingIncomeLoss'] = self.xbrl.GetFactValue("us-gaap:NonoperatingIncomeExpense",
                                                                                "Duration")

        # InterestAndDebtExpense
        self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue("us-gaap:InterestAndDebtExpense",
                                                                            "Duration")
        if self.xbrl.fields['InterestAndDebtExpense'] is None:
            self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue("us-gaap:InterestAndDebtExpense",
                                                                                "Duration")

        # IncomeBeforeEquityMethodInvestments
        self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.GetFactValue(
            "us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
            "Duration")

        # IncomeFromEquityMethodInvestments
        self.xbrl.fields['IncomeFromEquityMethodInvestments'] = self.xbrl.GetFactValue(
            "us-gaap:IncomeLossFromEquityMethodInvestments", "Duration")
        if self.xbrl.fields['IncomeFromEquityMethodInvestments'] is None:
            self.xbrl.fields['IncomeFromEquityMethodInvestments'] = self.xbrl.GetFactValue(
                "us-gaap:IncomeLossFromEquityMethodInvestments", "Duration")

        # IncomeFromContinuingOperationsBeforeTax
        self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue(
            "us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
            "Duration")
        if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] is None:
            self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue(
                "us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                "Duration")

        # IncomeTaxExpenseBenefit
        self.xbrl.fields['IncomeTaxExpenseBenefit'] = self.xbrl.GetFactValue("us-gaap:IncomeTaxExpenseBenefit",
                                                                             "Duration")
        if self.xbrl.fields['IncomeTaxExpenseBenefit'] is None:
            self.xbrl.fields['IncomeTaxExpenseBenefit'] = self.xbrl.GetFactValue(
                "us-gaap:IncomeTaxExpenseBenefitContinuingOperations", "Duration")

        # IncomeFromContinuingOperationsAfterTax
        self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.GetFactValue(
            "us-gaap:IncomeLossBeforeExtraordinaryItemsAndCumulativeEffectOfChangeInAccountingPrinciple", "Duration")
        if self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] is None:
            self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.GetFactValue(
                "us-gaap:IncomeLossBeforeExtraordinaryItemsAndCumulativeEffectOfChangeInAccountingPrinciple",
                "Duration")

        # IncomeFromDiscontinuedOperations
        self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue(
            "us-gaap:IncomeLossFromDiscontinuedOperationsNetOfTax", "Duration")
        if self.xbrl.fields['IncomeFromDiscontinuedOperations'] is None:
            self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue(
                "us-gaap:DiscontinuedOperationGainLossOnDisposalOfDiscontinuedOperationNetOfTax", "Duration")
            if self.xbrl.fields['IncomeFromDiscontinuedOperations'] is None:
                self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue(
                    "us-gaap:IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity", "Duration")

        # ExtraordaryItemsGainLoss
        self.xbrl.fields['ExtraordaryItemsGainLoss'] = self.xbrl.GetFactValue("us-gaap:ExtraordinaryItemNetOfTax",
                                                                              "Duration")
        if self.xbrl.fields['ExtraordaryItemsGainLoss'] is None:
            self.xbrl.fields['ExtraordaryItemsGainLoss'] = self.xbrl.GetFactValue("us-gaap:ExtraordinaryItemNetOfTax",
                                                                                  "Duration")

        # NetIncomeLoss
        self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("us-gaap:ProfitLoss", "Duration")
        if self.xbrl.fields['NetIncomeLoss'] is None:
            self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("us-gaap:NetIncomeLoss", "Duration")
            if self.xbrl.fields['NetIncomeLoss'] is None:
                self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue(
                    "us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic", "Duration")
                if self.xbrl.fields['NetIncomeLoss'] is None:
                    self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue(
                        "us-gaap:IncomeLossFromContinuingOperations", "Duration")
                    if self.xbrl.fields['NetIncomeLoss'] is None:
                        self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue(
                            "us-gaap:IncomeLossAttributableToParent", "Duration")
                        if self.xbrl.fields['NetIncomeLoss'] is None:
                            self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue(
                                "us-gaap:IncomeLossFromContinuingOperationsIncludingPortionAttributableToNoncontrollingInterest",
                                "Duration")

        #self.xbrl.fields['NetIncomeAttributableToShareholders'] = self.xbrl.GetFactValue(
        #    "us-gaap:ProfitLossAttributableToOwnersOfParent", "Duration")
        #if self.xbrl.fields['NetIncomeAttributableToShareholders'] is None:
        #    self.xbrl.fields['NetIncomeAttributableToShareholders'] = self.xbrl.fields['NetIncomeLoss']

        # NetIncomeAvailableToCommonStockholdersBasic
        self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] = self.xbrl.GetFactValue(
            "us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic", "Duration")

        # PreferredStockDividendsAndOtherAdjustments
        self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] = self.xbrl.GetFactValue(
            "us-gaap:PreferredStockDividendsAndOtherAdjustments", "Duration")

        # NetIncomeAttributableToNoncontrollingInterest
        self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue(
            "us-gaap:NetIncomeLossAttributableToNoncontrollingInterest", "Duration")

        # NetIncomeAttributableToParent
        self.xbrl.fields['NetIncomeAttributableToParent'] = self.xbrl.GetFactValue("us-gaap:NetIncomeLoss", "Duration")

        # OtherComprehensiveIncome
        self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.GetFactValue(
            "us-gaap:OtherComprehensiveIncomeLossNetOfTax", "Duration")
        if self.xbrl.fields['OtherComprehensiveIncome'] is None:
            self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.GetFactValue(
                "us-gaap:OtherComprehensiveIncomeLossNetOfTax", "Duration")

        # ComprehensiveIncome
        self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.GetFactValue(
            "us-gaap:ComprehensiveIncomeNetOfTaxIncludingPortionAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['ComprehensiveIncome'] is None:
            self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.GetFactValue("us-gaap:ComprehensiveIncomeNetOfTax",
                                                                             "Duration")

        # ComprehensiveIncomeAttributableToParent
        self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.GetFactValue(
            "us-gaap:ComprehensiveIncomeNetOfTax", "Duration")
        if self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] is None:
            self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.GetFactValue(
                "us-gaap:ComprehensiveIncomeNetOfTax", "Duration")

        # ComprehensiveIncomeAttributableToNoncontrollingInterest
        self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue(
            "us-gaap:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] is None:
            self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue(
                "us-gaap:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "Duration")

        #########'Adjustments to income statement information
        # Impute: NonoperatingIncomeLossPlusInterestAndDebtExpense
        if self.xbrl.fields['NonoperatingIncomeLoss'] is not None \
                and self.xbrl.fields['InterestAndDebtExpense'] is not None:
            self.xbrl.fields['NonoperatingIncomeLossPlusInterestAndDebtExpense'] = self.xbrl.fields[
                                                                                       'NonoperatingIncomeLoss'] + \
                                                                                   self.xbrl.fields[
                                                                                       'InterestAndDebtExpense']

        # Impute: Net income available to common stockholders  (if it does not exist)
        if self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] is None \
                and self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] is None \
                and self.xbrl.fields['NetIncomeAttributableToParent'] is not None:
            self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] = self.xbrl.fields[
                'NetIncomeAttributableToParent']

        # Impute NetIncomeLoss
        if self.xbrl.fields['NetIncomeLoss'] is not None \
                and self.xbrl.fields['IncomeFromDiscontinuedOperations'] is not None \
                and self.xbrl.fields['ExtraordaryItemsGainLoss'] is not None \
                and self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] is None:
            self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.fields['NetIncomeLoss'] - \
                                                                         self.xbrl.fields[
                                                                             'IncomeFromDiscontinuedOperations'] - \
                                                                         self.xbrl.fields['ExtraordaryItemsGainLoss']

        # Impute: Net income attributable to parent if it does not exist
        if self.xbrl.fields['NetIncomeAttributableToParent'] is None \
                and self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest'] is None \
                and self.xbrl.fields['NetIncomeLoss'] is not None:
            self.xbrl.fields['NetIncomeAttributableToParent'] = self.xbrl.fields['NetIncomeLoss']

        # Impute: PreferredStockDividendsAndOtherAdjustments
        if self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] is None \
                and self.xbrl.fields['NetIncomeAttributableToParent'] is not None \
                and self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] is not None:
            self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] = self.xbrl.fields[
                                                                                 'NetIncomeAttributableToParent'] - \
                                                                             self.xbrl.fields[
                                                                                 'NetIncomeAvailableToCommonStockholdersBasic']

        # Impute: comprehensive income
        if self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] is None \
                and self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] is None \
                and self.xbrl.fields['ComprehensiveIncome'] is None \
                and self.xbrl.fields['OtherComprehensiveIncome'] is None:
            self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.fields['NetIncomeLoss']

        # Impute: other comprehensive income
        if self.xbrl.fields['ComprehensiveIncome'] is not None \
                and self.xbrl.fields['NetIncomeLoss'] is not None \
                and self.xbrl.fields['OtherComprehensiveIncome'] is None:
            self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.fields['ComprehensiveIncome'] - \
                                                           self.xbrl.fields['NetIncomeLoss']

        # Impute: comprehensive income attributable to parent if it does not exist
        if self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] is None \
                and self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] is None \
                and self.xbrl.fields['ComprehensiveIncome'] is not None:
            self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.fields['ComprehensiveIncome']

        # Impute: IncomeFromContinuingOperations*Before*Tax
        if self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] is not None \
                and self.xbrl.fields['IncomeFromEquityMethodInvestments'] is not None \
                and self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] is None:
            self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.fields[
                                                                              'IncomeBeforeEquityMethodInvestments'] + \
                                                                          self.xbrl.fields[
                                                                              'IncomeFromEquityMethodInvestments']

        # Impute: IncomeFromContinuingOperations*Before*Tax2 (if income before tax is missing)
        if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] is None \
                and self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] is not None \
                and self.xbrl.fields['IncomeTaxExpenseBenefit'] is not None:
            self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.fields[
                                                                              'IncomeFromContinuingOperationsAfterTax'] + \
                                                                          self.xbrl.fields['IncomeTaxExpenseBenefit']

        # Impute: IncomeFromContinuingOperations*After*Tax
        if self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] is None \
                and self.xbrl.fields['IncomeTaxExpenseBenefit'] is not None \
                and self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] is not None:
            self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.fields[
                                                                             'IncomeFromContinuingOperationsBeforeTax'] - \
                                                                         self.xbrl.fields['IncomeTaxExpenseBenefit']

        # Impute: GrossProfit
        if self.xbrl.fields['GrossProfit'] is None \
                and self.xbrl.fields['Revenues'] is not None \
                and self.xbrl.fields['CostOfRevenue'] is not None:
            self.xbrl.fields['GrossProfit'] = self.xbrl.fields['Revenues'] - self.xbrl.fields['CostOfRevenue']

        # Impute: Revenues
        if self.xbrl.fields['GrossProfit'] is not None \
                and self.xbrl.fields['Revenues'] is None \
                and self.xbrl.fields['CostOfRevenue'] is not None:
            self.xbrl.fields['Revenues'] = self.xbrl.fields['GrossProfit'] + self.xbrl.fields['CostOfRevenue']

        # Impute: CostOfRevenue
        if self.xbrl.fields['GrossProfit'] is not None \
                and self.xbrl.fields['Revenues'] is not None \
                and self.xbrl.fields['CostOfRevenue'] is None:
            self.xbrl.fields['CostOfRevenue'] = self.xbrl.fields['GrossProfit'] + self.xbrl.fields['Revenues']

        # Impute: CostsAndExpenses (would NEVER have costs and expenses if has gross profit, gross profit is multi-step and costs and expenses is single-step)
        if self.xbrl.fields['GrossProfit'] is None \
                and self.xbrl.fields['CostsAndExpenses'] is None \
                and self.xbrl.fields['CostOfRevenue'] is not None \
                and self.xbrl.fields['OperatingExpenses'] is not None:
            self.xbrl.fields['CostsAndExpenses'] = self.xbrl.fields['CostOfRevenue'] + \
                                                   self.xbrl.fields['OperatingExpenses']

        # Impute: CostsAndExpenses based on existance of both costs of revenues and operating expenses
        if self.xbrl.fields['CostsAndExpenses'] is None \
                and self.xbrl.fields['OperatingExpenses'] is not None \
                and self.xbrl.fields['CostOfRevenue'] is not None:
            self.xbrl.fields['CostsAndExpenses'] = self.xbrl.fields['CostOfRevenue'] + \
                                                   self.xbrl.fields['OperatingExpenses']

        # Impute: CostsAndExpenses
        if self.xbrl.fields['GrossProfit'] is None \
                and self.xbrl.fields['CostsAndExpenses'] is None \
                and self.xbrl.fields['Revenues'] is not None \
                and self.xbrl.fields['OperatingIncomeLoss'] is not None \
                and self.xbrl.fields['OtherOperatingIncome'] is not None:
            self.xbrl.fields['CostsAndExpenses'] = self.xbrl.fields['Revenues'] - \
                                                   self.xbrl.fields['OperatingIncomeLoss'] - \
                                                   self.xbrl.fields['OtherOperatingIncome']

        # Impute: OperatingExpenses based on existance of costs and expenses and cost of revenues
        if self.xbrl.fields['CostOfRevenue'] is not None \
                and self.xbrl.fields['CostsAndExpenses'] is not None \
                and self.xbrl.fields['OperatingExpenses'] is None:
            self.xbrl.fields['OperatingExpenses'] = self.xbrl.fields['CostsAndExpenses'] - \
                                                    self.xbrl.fields['CostOfRevenue']

        # Impute: CostOfRevenues single-step method
        if self.xbrl.fields['Revenues'] is not None \
                and self.xbrl.fields['CostsAndExpenses'] is not None \
                and self.xbrl.fields['GrossProfit'] is None \
                and (self.xbrl.fields['OperatingIncomeLoss'] ==
                     self.xbrl.fields['Revenues'] - self.xbrl.fields['CostsAndExpenses']) \
                and self.xbrl.fields['OperatingExpenses'] is None \
                and self.xbrl.fields['OtherOperatingIncome'] is None:
            self.xbrl.fields['CostOfRevenue'] = self.xbrl.fields['CostsAndExpenses'] - \
                                                self.xbrl.fields['OperatingExpenses']

        # Impute: IncomeBeforeEquityMethodInvestments
        if self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] is None \
                and self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] is not None \
                and self.xbrl.fields['IncomeFromEquityMethodInvestments'] is not None:
            self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.fields[
                                                                          'IncomeFromContinuingOperationsBeforeTax'] - \
                                                                      self.xbrl.fields[
                                                                          'IncomeFromEquityMethodInvestments']

        # Impute: IncomeBeforeEquityMethodInvestments
        if self.xbrl.fields['OperatingIncomeLoss'] is not None \
                and self.xbrl.fields['NonoperatingIncomeLoss'] is not None \
                and self.xbrl.fields['InterestAndDebtExpense'] is None \
                and self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] is not None:
            self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] - (
                    self.xbrl.fields['OperatingIncomeLoss'] + self.xbrl.fields['NonoperatingIncomeLoss'])

        # Impute: OtherOperatingIncome
        if self.xbrl.fields['OtherOperatingIncome'] is None \
                and self.xbrl.fields['GrossProfit'] is not None \
                and self.xbrl.fields['OperatingExpenses'] is not None \
                and self.xbrl.fields['OperatingIncomeLoss'] is not None:
            self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.fields['OperatingIncomeLoss'] - (
                    self.xbrl.fields['GrossProfit'] - self.xbrl.fields['OperatingExpenses'])

        # Move IncomeFromEquityMethodInvestments
        if self.xbrl.fields['IncomeFromEquityMethodInvestments'] is not None \
                and self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] is not None \
                and self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] is not None \
                and self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] != self.xbrl.fields[
            'IncomeFromContinuingOperationsBeforeTax']:
            self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.fields[
                                                                          'IncomeFromContinuingOperationsBeforeTax'] - \
                                                                      self.xbrl.fields[
                                                                          'IncomeFromEquityMethodInvestments']
            if self.xbrl.fields['OperatingIncomeLoss'] is not None:
                self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.fields['OperatingIncomeLoss'] - \
                                                          self.xbrl.fields['IncomeFromEquityMethodInvestments']

        # DANGEROUS!!  May need to turn off. IS3 had 2085 PASSES WITHOUT this imputing. if it is higher,: keep the test
        # Impute: OperatingIncomeLoss
        if self.xbrl.fields['OperatingIncomeLoss'] is None \
                and self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] is not None \
                and self.xbrl.fields['NonoperatingIncomeLoss'] is not None \
                and self.xbrl.fields['InterestAndDebtExpense'] is not None:
            self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] + \
                                                      self.xbrl.fields['NonoperatingIncomeLoss'] - \
                                                      self.xbrl.fields['InterestAndDebtExpense']

        if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] is not None \
                and self.xbrl.fields['OperatingIncomeLoss'] is not None:
            self.xbrl.fields['NonoperatingIncomePlusInterestAndDebtExpensePlusIncomeFromEquityMethodInvestments'] = \
                self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] - self.xbrl.fields['OperatingIncomeLoss']

        # NonoperatingIncomeLossPlusInterestAndDebtExpense
        if self.xbrl.fields['NonoperatingIncomeLossPlusInterestAndDebtExpense'] is None \
                and self.xbrl.fields[
            'NonoperatingIncomePlusInterestAndDebtExpensePlusIncomeFromEquityMethodInvestments'] is not None \
                and self.xbrl.fields['IncomeFromEquityMethodInvestments'] is not None:
            self.xbrl.fields['NonoperatingIncomeLossPlusInterestAndDebtExpense'] = self.xbrl.fields[
                                                                                       'NonoperatingIncomePlusInterestAndDebtExpensePlusIncomeFromEquityMethodInvestments'] - \
                                                                                   self.xbrl.fields[
                                                                                       'IncomeFromEquityMethodInvestments']

        ###Cash flow statement

        # NetCashFlow
        self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("us-gaap:CashAndCashEquivalentsPeriodIncreaseDecrease",
                                                                 "Duration")
        if self.xbrl.fields['NetCashFlow'] is None:
            self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("us-gaap:CashPeriodIncreaseDecrease", "Duration")
            if self.xbrl.fields['NetCashFlow'] is None:
                self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue(
                    "us-gaap:NetCashProvidedByUsedInContinuingOperations", "Duration")

        # NetCashFlowsOperating
        self.xbrl.fields['NetCashFlowsOperating'] = self.xbrl.GetFactValue(
            "us-gaap:NetCashProvidedByUsedInOperatingActivities", "Duration")

        # NetCashFlowsInvesting
        self.xbrl.fields['NetCashFlowsInvesting'] = self.xbrl.GetFactValue(
            "us-gaap:NetCashProvidedByUsedInInvestingActivities", "Duration")

        # NetCashFlowsFinancing
        self.xbrl.fields['NetCashFlowsFinancing'] = self.xbrl.GetFactValue(
            "us-gaap:NetCashProvidedByUsedInFinancingActivities", "Duration")

        # NetCashFlowsOperatingContinuing
        self.xbrl.fields['NetCashFlowsOperatingContinuing'] = self.xbrl.GetFactValue(
            "us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations", "Duration")

        # NetCashFlowsInvestingContinuing
        self.xbrl.fields['NetCashFlowsInvestingContinuing'] = self.xbrl.GetFactValue(
            "us-gaap:NetCashProvidedByUsedInInvestingActivitiesContinuingOperations", "Duration")

        # NetCashFlowsFinancingContinuing
        self.xbrl.fields['NetCashFlowsFinancingContinuing'] = self.xbrl.GetFactValue(
            "us-gaap:NetCashProvidedByUsedInFinancingActivitiesContinuingOperations", "Duration")

        # NetCashFlowsOperatingDiscontinued
        self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] = self.xbrl.GetFactValue(
            "us-gaap:CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations", "Duration")

        # NetCashFlowsInvestingDiscontinued
        self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] = self.xbrl.GetFactValue(
            "us-gaap:CashProvidedByUsedInInvestingActivitiesDiscontinuedOperations", "Duration")

        # NetCashFlowsFinancingDiscontinued
        self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] = self.xbrl.GetFactValue(
            "us-gaap:CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", "Duration")

        # NetCashFlowsDiscontinued
        self.xbrl.fields['NetCashFlowsDiscontinued'] = self.xbrl.GetFactValue(
            "us-gaap:NetCashProvidedByUsedInDiscontinuedOperations", "Duration")

        # ExchangeGainsLosses
        self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue(
            "us-gaap:EffectOfExchangeRateOnCashAndCashEquivalents", "Duration")
        if self.xbrl.fields['ExchangeGainsLosses'] is None:
            self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue(
                "us-gaap:EffectOfExchangeRateOnCashAndCashEquivalentsContinuingOperations", "Duration")
            if self.xbrl.fields['ExchangeGainsLosses'] is None:
                self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue(
                    "us-gaap:CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", "Duration")

        ####Adjustments
        # Impute: total net cash flows discontinued if not reported
        if self.xbrl.fields['NetCashFlowsDiscontinued'] is None \
                and self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] is not None \
                and self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] is not None \
                and self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] is not None:
            self.xbrl.fields['NetCashFlowsDiscontinued'] = self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] + \
                                                           self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] + \
                                                           self.xbrl.fields['NetCashFlowsFinancingDiscontinued']

        # Impute: cash flows from continuing
        if self.xbrl.fields['NetCashFlowsOperating'] is not None \
                and self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] is not None \
                and self.xbrl.fields['NetCashFlowsOperatingContinuing'] is None:
            self.xbrl.fields['NetCashFlowsOperatingContinuing'] = self.xbrl.fields['NetCashFlowsOperating'] - \
                                                                  self.xbrl.fields['NetCashFlowsOperatingDiscontinued']

        if self.xbrl.fields['NetCashFlowsInvesting'] is not None \
                and self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] is not None \
                and self.xbrl.fields['NetCashFlowsInvestingContinuing'] is None:
            self.xbrl.fields['NetCashFlowsInvestingContinuing'] = self.xbrl.fields['NetCashFlowsInvesting'] - \
                                                                  self.xbrl.fields['NetCashFlowsInvestingDiscontinued']

        if self.xbrl.fields['NetCashFlowsFinancing'] is not None \
                and self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] is not None \
                and self.xbrl.fields['NetCashFlowsFinancingContinuing'] is None:
            self.xbrl.fields['NetCashFlowsFinancingContinuing'] = self.xbrl.fields['NetCashFlowsFinancing'] - \
                                                                  self.xbrl.fields['NetCashFlowsFinancingDiscontinued']

        if self.xbrl.fields['NetCashFlowsOperating'] is None \
                and self.xbrl.fields['NetCashFlowsOperatingContinuing'] is not None \
                and self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] is None:
            self.xbrl.fields['NetCashFlowsOperating'] = self.xbrl.fields['NetCashFlowsOperatingContinuing']

        if self.xbrl.fields['NetCashFlowsInvesting'] is None \
                and self.xbrl.fields['NetCashFlowsInvestingContinuing'] is not None \
                and self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] is None:
            self.xbrl.fields['NetCashFlowsInvesting'] = self.xbrl.fields['NetCashFlowsInvestingContinuing']

        if self.xbrl.fields['NetCashFlowsFinancing'] is None \
                and self.xbrl.fields['NetCashFlowsFinancingContinuing'] is not None \
                and self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] is None:
            self.xbrl.fields['NetCashFlowsFinancing'] = self.xbrl.fields['NetCashFlowsFinancingContinuing']

        if self.xbrl.fields['NetCashFlowsOperatingContinuing'] is not None \
                and self.xbrl.fields['NetCashFlowsInvestingContinuing'] is not None \
                and self.xbrl.fields['NetCashFlowsFinancingContinuing'] is not None:
            self.xbrl.fields['NetCashFlowsContinuing'] = self.xbrl.fields['NetCashFlowsOperatingContinuing'] + \
                                                         self.xbrl.fields['NetCashFlowsInvestingContinuing'] + \
                                                         self.xbrl.fields['NetCashFlowsFinancingContinuing']

        # Impute: if net cash flow is missing,: this tries to figure out the value by adding up the detail
        if self.xbrl.fields['NetCashFlow'] is None \
                and (self.xbrl.fields['NetCashFlowsOperating'] is not None
                     or self.xbrl.fields['NetCashFlowsInvesting'] is not None
                     or self.xbrl.fields['NetCashFlowsFinancing'] is not None):
            operating_val = 0
            investing_val = 0
            financing_val = 0
            unit_ref = None

            if self.xbrl.fields['NetCashFlowsOperating']:
                unit_ref = self.xbrl.fields['NetCashFlowsOperating'].unit_ref
                operating_val = self.xbrl.fields['NetCashFlowsOperating'].value
            if self.xbrl.fields['NetCashFlowsInvesting']:
                unit_ref = self.xbrl.fields['NetCashFlowsInvesting'].unit_ref
                investing_val = self.xbrl.fields['NetCashFlowsInvesting'].value
            if self.xbrl.fields['NetCashFlowsFinancing']:
                unit_ref = self.xbrl.fields['NetCashFlowsFinancing'].unit_ref
                financing_val = self.xbrl.fields['NetCashFlowsFinancing'].value

            from edgar_data.xbrl import Field
            self.xbrl.fields['NetCashFlow'] = Field(operating_val + investing_val + financing_val, unit_ref)

        # Key ratios
        try:
            self.xbrl.fields['SGR'] = ((self.xbrl.fields['NetIncomeLoss'] / self.xbrl.fields['Revenues']) * (1 + (
                    (self.xbrl.fields['Assets'] - self.xbrl.fields['Equity']) / self.xbrl.fields['Equity']))) / (
                                              (1 / (self.xbrl.fields['Revenues'] / self.xbrl.fields['Assets'])) - ((
                                              (self.xbrl.fields['NetIncomeLoss'] / self.xbrl.fields[
                                                  'Revenues']) * (1 + ((
                                              (self.xbrl.fields['Assets'] - self.xbrl.fields['Equity']) /
                                              self.xbrl.fields['Equity']))))))
        except:
            pass

        try:
            self.xbrl.fields['ROA'] = self.xbrl.fields['NetIncomeLoss'] / self.xbrl.fields['Assets']
        except:
            pass

        try:
            self.xbrl.fields['ROE'] = self.xbrl.fields['NetIncomeLoss'] / self.xbrl.fields['Equity']
        except:
            pass

        try:
            self.xbrl.fields['ROS'] = self.xbrl.fields['NetIncomeLoss'] / self.xbrl.fields['Revenues']
        except:
            pass

        self.xbrl.fields['ResearchAndDevelopmentExpense'] = self.xbrl.GetFactValue(
            'us-gaap:ResearchAndDevelopmentExpense', 'Duration')

        try:
            self.ifrs()
        except:
            pass

    def ifrs(self):
        """
        Labels found at:
        https://www.ifrs.org/-/media/feature/standards/taxonomy/2018/2018-taxonomy-view-with-definitions.xlsx?la=en&hash=5532C37EEAD057F62AA9AA1C920E33F43B3140FD
        """

        # These are the ones also found on GAAP:
        if self.xbrl.fields['Revenues'] is None:
            self.xbrl.fields['Revenues'] = self.xbrl.GetFactValue('ifrs-full:Revenue', 'Duration')

        if self.xbrl.fields['NetIncomeAttributableToParent'] is None:
            self.xbrl.fields['NetIncomeAttributableToParent'] = self.xbrl.GetFactValue(
                "ifrs-full:ProfitLossAttributableToOwnersOfParent", "Duration")

        if self.xbrl.fields['Assets'] is None:
            self.xbrl.fields['Assets'] = self.xbrl.GetFactValue('ifrs-full:Assets', 'Instant')

        if self.xbrl.fields['CurrentAssets'] is None:
            self.xbrl.fields['CurrentAssets'] = self.xbrl.GetFactValue('ifrs-full:CurrentAssets', 'Instant')

        if self.xbrl.fields['NoncurrentAssets'] is None:
            self.xbrl.fields['NoncurrentAssets'] = self.xbrl.GetFactValue('ifrs-full:NoncurrentAssets', 'Instant')

        if self.xbrl.fields['Liabilities'] is None:
            self.xbrl.fields['Liabilities'] = self.xbrl.GetFactValue('ifrs-full:Liabilities', 'Instant')

        if self.xbrl.fields['CurrentLiabilities'] is None:
            self.xbrl.fields['CurrentLiabilities'] = self.xbrl.GetFactValue('ifrs-full:CurrentLiabilities',
                                                                            'Instant')

        if self.xbrl.fields['NoncurrentLiabilities'] is None:
            self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.GetFactValue('ifrs-full:NoncurrentLiabilities',
                                                                               'Instant')

        if self.xbrl.fields['LiabilitiesAndEquity'] is None:
            self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue('ifrs-full:EquityAndLiabilities',
                                                                              'Instant')

        if self.xbrl.fields['Equity'] is None:
            self.xbrl.fields['Equity'] = self.xbrl.GetFactValue('ifrs-full:Equity', 'Instant')

        if self.xbrl.fields['CostOfRevenue'] is None:
            self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue('ifrs-full:CostOfSales', 'Duration')

        if self.xbrl.fields['GrossProfit'] is None:
            self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue('ifrs-full:GrossProfit', 'Duration')

        if self.xbrl.fields['NetCashFlowsOperating'] is None:
            self.xbrl.fields['NetCashFlowsOperating'] = self.xbrl.GetFactValue(
                'ifrs-full:CashFlowsFromUsedInOperatingActivities', 'Duration')

        if self.xbrl.fields['NetCashFlowsInvesting'] is None:
            self.xbrl.fields['NetCashFlowsInvesting'] = self.xbrl.GetFactValue(
                'ifrs-full:CashFlowsFromUsedInInvestingActivities', 'Duration')

        if self.xbrl.fields['NetCashFlowsFinancing'] is None:
            self.xbrl.fields['NetCashFlowsFinancing'] = self.xbrl.GetFactValue(
                'ifrs-full:CashFlowsFromUsedInFinancingActivities', 'Duration')

        if self.xbrl.fields['NetCashFlow'] is None:
            # Might also try to use IncreaseDecreaseInCashAndCashEquivalentsBeforeEffectOfExchangeRateChanges ??
            # Makes sense since many 20-F forms can use foreign currencies
            self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue(
                'ifrs-full:IncreaseDecreaseInCashAndCashEquivalents', 'Duration')
            if self.xbrl.fields['NetCashFlow'] is None:
                self.xbrl.fields['NetCashFlow'] = self.xbrl.fields['NetCashFlowsOperating'] + \
                                                  self.xbrl.fields['NetCashFlowsInvesting'] + \
                                                  self.xbrl.fields['NetCashFlowsFinancing']

        if self.xbrl.fields['OperatingExpenses'] is None:
            self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue('ifrs-full:OperatingExpense',
                                                                           'Duration')

        if self.xbrl.fields['OperatingIncomeLoss'] is None:
            self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue('ifrs-full:ProfitLossBeforeTax',
                                                                             'Duration')

        if self.xbrl.fields['InterestAndDebtExpense'] is None:
            self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue('ifrs-full:InterestExpense',
                                                                                'Duration')

        if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] is None:
            self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue(
                'ifrs-full:ProfitLossBeforeTax', 'Duration')

        if self.xbrl.fields['NetIncomeLoss'] is None:
            self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue('ifrs-full:ProfitLoss', 'Duration')

        if self.xbrl.fields['ResearchAndDevelopmentExpense'] is None:
            self.xbrl.fields['ResearchAndDevelopmentExpense'] = self.xbrl.GetFactValue(
                'ifrs-full:ResearchAndDevelopmentExpense', 'Duration')

        # These are the ones not found on pysec GAAP parsing:

        self.xbrl.fields['SellingGeneralAndAdministrativeExpense'] = self.xbrl.GetFactValue(
            'ifrs-full:SellingGeneralAndAdministrativeExpense', 'Duration')

        self.xbrl.fields['RentalExpenses'] = self.xbrl.GetFactValue('ifrs-full:RentalExpense', 'Duration')

        self.xbrl.fields['RepairsAndMaintenanceExpense'] = self.xbrl.GetFactValue(
            'ifrs-full:RepairsAndMaintenanceExpense', 'Duration')

        self.xbrl.fields['SalesAndMarketingExpense'] = self.xbrl.GetFactValue('ifrs-full:SalesAndMarketingExpense',
                                                                              'Duration')

