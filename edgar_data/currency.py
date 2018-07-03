# Adapted from python-money:
# https://github.com/poswald/python-money
import re
from collections import namedtuple, defaultdict

Currency = namedtuple('Currency', ['code', 'symbol', 'name'])

currency_identifiers = {}

iso_currency_re = re.compile('iso4217_?[A-Z]{3}')


def possible_currency_from_unit_ref(unit_ref):
    yield unit_ref[:3]
    yield unit_ref[-3:]
    iso_match = iso_currency_re.search(unit_ref)
    if iso_match:
        yield iso_match.group()[-3:]


def find_currency(unit_ref):
    unit_ref = unit_ref.upper()

    for possible_currency in possible_currency_from_unit_ref(unit_ref):
        if possible_currency in currency_identifiers:
            return currency_identifiers[possible_currency]


currency_identifiers['AED'] = Currency('AED', u'', u'UAE Dirham')
currency_identifiers['AFN'] = Currency('AFN', u'؋', u'Afghani')
currency_identifiers['ALL'] = Currency('ALL', u'Lek', u'Lek')
currency_identifiers['AMD'] = Currency('AMD', u'', u'Armenian Dram')
currency_identifiers['ANG'] = Currency('ANG', u'ƒ', u'Netherlands Antillean Guilder')
currency_identifiers['AOA'] = Currency('AOA', u'', u'Kwanza')
currency_identifiers['ARS'] = Currency('ARS', u'$', u'Argentine Peso')
currency_identifiers['AUD'] = Currency('AUD', u'$', u'Australian Dollar')
currency_identifiers['AWG'] = Currency('AWG', u'ƒ', u'Aruban Florin')
currency_identifiers['AZN'] = Currency('AZN', u'ман', u'Azerbaijanian Manat')
currency_identifiers['BAM'] = Currency('BAM', u'KM', u'Convertible Mark')
currency_identifiers['BBD'] = Currency('BBD', u'$', u'Barbados Dollar')
currency_identifiers['BDT'] = Currency('BDT', u'', u'Taka')
currency_identifiers['BGN'] = Currency('BGN', u'лв', u'Bulgarian Lev')
currency_identifiers['BHD'] = Currency('BHD', u'', u'Bahraini Dinar')
currency_identifiers['BIF'] = Currency('BIF', u'', u'Burundi Franc')
currency_identifiers['BMD'] = Currency('BMD', u'$', u'Bermudian Dollar')
currency_identifiers['BND'] = Currency('BND', u'$', u'Brunei Dollar')
currency_identifiers['BOB'] = Currency('BOB', u'$b', u'Boliviano')
currency_identifiers['BOV'] = Currency('BOV', u'', u'Mvdol')
currency_identifiers['BRL'] = Currency('BRL', u'R$', u'Brazilian Real')
currency_identifiers['BSD'] = Currency('BSD', u'$', u'Bahamian Dollar')
currency_identifiers['BTN'] = Currency('BTN', u'', u'Ngultrum')
currency_identifiers['BWP'] = Currency('BWP', u'P', u'Pula')
currency_identifiers['BYR'] = Currency('BYR', u'p.', u'Belarussian Ruble')
currency_identifiers['BZD'] = Currency('BZD', u'BZ$', u'Belize Dollar')
currency_identifiers['CAD'] = Currency('CAD', u'$', u'Canadian Dollar')
currency_identifiers['CDF'] = Currency('CDF', u'', u'Congolese Franc')
currency_identifiers['CHE'] = Currency('CHE', u'', u'WIR Euro')
currency_identifiers['CHF'] = Currency('CHF', u'Fr.', u'Swiss Franc')
currency_identifiers['CHW'] = Currency('CHW', u'', u'WIR Franc')
currency_identifiers['CLF'] = Currency('CLF', u'', u'Unidades de fomento')
currency_identifiers['CLP'] = Currency('CLP', u'$', u'Chilean Peso')
currency_identifiers['CNY'] = Currency('CNY', u'¥', u'Yuan Renminbi')
currency_identifiers['COP'] = Currency('COP', u'$', u'Colombian Peso')
currency_identifiers['COU'] = Currency('COU', u'', u'Unidad de Valor Real')
currency_identifiers['CRC'] = Currency('CRC', u'₡', u'Costa Rican Colon')
currency_identifiers['CUC'] = Currency('CUC', u'', u'Peso Convertible')
currency_identifiers['CUP'] = Currency('CUP', u'₱', u'Cuban Peso')
currency_identifiers['CVE'] = Currency('CVE', u'', u'Cape Verde Escudo')
currency_identifiers['CZK'] = Currency('CZK', u'Kč', u'Czech Koruna')
currency_identifiers['DJF'] = Currency('DJF', u'', u'Djibouti Franc')
currency_identifiers['DKK'] = Currency('DKK', u'kr', u'Danish Krone')
currency_identifiers['DOP'] = Currency('DOP', u'RD$', u'Dominican Peso')
currency_identifiers['DZD'] = Currency('DZD', u'', u'Algerian Dinar')
currency_identifiers['EGP'] = Currency('EGP', u'£', u'Egyptian Pound')
currency_identifiers['ERN'] = Currency('ERN', u'', u'Nakfa')
currency_identifiers['ETB'] = Currency('ETB', u'', u'Ethiopian Birr')
currency_identifiers['EUR'] = Currency('EUR', u'€', u'Euro')
currency_identifiers['FJD'] = Currency('FJD', u'$', u'Fiji Dollar')
currency_identifiers['FKP'] = Currency('FKP', u'£', u'Falkland Islands Pound')
currency_identifiers['GBP'] = Currency('GBP', u'£', u'Pound Sterling')
currency_identifiers['GEL'] = Currency('GEL', u'', u'Lari')
currency_identifiers['GHS'] = Currency('GHS', u'', u'Ghana Cedi')
currency_identifiers['GIP'] = Currency('GIP', u'£', u'Gibraltar Pound')
currency_identifiers['GMD'] = Currency('GMD', u'', u'Dalasi')
currency_identifiers['GNF'] = Currency('GNF', u'', u'Guinea Franc')
currency_identifiers['GTQ'] = Currency('GTQ', u'Q', u'Quetzal')
currency_identifiers['GYD'] = Currency('GYD', u'$', u'Guyana Dollar')
currency_identifiers['HKD'] = Currency('HKD', u'HK$', u'Hong Kong Dollar')
currency_identifiers['HNL'] = Currency('HNL', u'L', u'Lempira')
currency_identifiers['HRK'] = Currency('HRK', u'kn', u'Croatian Kuna')
currency_identifiers['HTG'] = Currency('HTG', u'', u'Gourde')
currency_identifiers['HUF'] = Currency('HUF', u'Ft', u'Forint')
currency_identifiers['IDR'] = Currency('IDR', u'Rp', u'Rupiah')
currency_identifiers['ILS'] = Currency('ILS', u'₪', u'New Israeli Sheqel')
currency_identifiers['INR'] = Currency('INR', u'', u'Indian Rupee')
currency_identifiers['IQD'] = Currency('IQD', u'', u'Iraqi Dinar')
currency_identifiers['IRR'] = Currency('IRR', u'﷼', u'Iranian Rial')
currency_identifiers['ISK'] = Currency('ISK', u'kr', u'Iceland Krona')
currency_identifiers['JMD'] = Currency('JMD', u'J$', u'Jamaican Dollar')
currency_identifiers['JOD'] = Currency('JOD', u'', u'Jordanian Dinar')
currency_identifiers['JPY'] = Currency('JPY', u'¥', u'Yen')
currency_identifiers['KES'] = Currency('KES', u'', u'Kenyan Shilling')
currency_identifiers['KGS'] = Currency('KGS', u'лв', u'Som')
currency_identifiers['KHR'] = Currency('KHR', u'៛', u'Riel')
currency_identifiers['KMF'] = Currency('KMF', u'', u'Comoro Franc')
currency_identifiers['KPW'] = Currency('KPW', u'₩', u'North Korean Won')
currency_identifiers['KRW'] = Currency('KRW', u'₩', u'Won')
currency_identifiers['KWD'] = Currency('KWD', u'', u'Kuwaiti Dinar')
currency_identifiers['KYD'] = Currency('KYD', u'$', u'Cayman Islands Dollar')
currency_identifiers['KZT'] = Currency('KZT', u'лв', u'Tenge')
currency_identifiers['LAK'] = Currency('LAK', u'₭', u'Kip')
currency_identifiers['LBP'] = Currency('LBP', u'£', u'Lebanese Pound')
currency_identifiers['LKR'] = Currency('LKR', u'₨', u'Sri Lanka Rupee')
currency_identifiers['LRD'] = Currency('LRD', u'$', u'Liberian Dollar')
currency_identifiers['LSL'] = Currency('LSL', u'', u'Loti')
currency_identifiers['LTL'] = Currency('LTL', u'Lt', u'Lithuanian Litas')
currency_identifiers['LVL'] = Currency('LVL', u'Ls', u'Latvian Lats')
currency_identifiers['LYD'] = Currency('LYD', u'', u'Libyan Dinar')
currency_identifiers['MAD'] = Currency('MAD', u'', u'Moroccan Dirham')
currency_identifiers['MDL'] = Currency('MDL', u'', u'Moldovan Leu')
currency_identifiers['MGA'] = Currency('MGA', u'', u'Malagasy Ariary')
currency_identifiers['MKD'] = Currency('MKD', u'ден', u'Denar')
currency_identifiers['MMK'] = Currency('MMK', u'', u'Kyat')
currency_identifiers['MNT'] = Currency('MNT', u'₮', u'Tugrik')
currency_identifiers['MOP'] = Currency('MOP', u'', u'Pataca')
currency_identifiers['MRO'] = Currency('MRO', u'', u'Ouguiya')
currency_identifiers['MUR'] = Currency('MUR', u'₨', u'Mauritius Rupee')
currency_identifiers['MVR'] = Currency('MVR', u'', u'Rufiyaa')
currency_identifiers['MWK'] = Currency('MWK', u'', u'Kwacha')
currency_identifiers['MXN'] = Currency('MXN', u'$', u'Mexican Peso')
currency_identifiers['MXV'] = Currency('MXV', u'', u'Mexican Unidad de Inversion (UDI)')
currency_identifiers['MYR'] = Currency('MYR', u'RM', u'Malaysian Ringgit')
currency_identifiers['MZN'] = Currency('MZN', u'MT', u'Mozambique Metical')
currency_identifiers['NAD'] = Currency('NAD', u'$', u'Namibia Dollar')
currency_identifiers['NGN'] = Currency('NGN', u'₦', u'Naira')
currency_identifiers['NIO'] = Currency('NIO', u'C$', u'Cordoba Oro')
currency_identifiers['NOK'] = Currency('NOK', u'kr', u'Norwegian Krone')
currency_identifiers['NPR'] = Currency('NPR', u'₨', u'Nepalese Rupee')
currency_identifiers['NZD'] = Currency('NZD', u'$', u'New Zealand Dollar')
currency_identifiers['OMR'] = Currency('OMR', u'﷼', u'Rial Omani')
currency_identifiers['PAB'] = Currency('PAB', u'B/.', u'Balboa')
currency_identifiers['PEN'] = Currency('PEN', u'S/.', u'Nuevo Sol')
currency_identifiers['PGK'] = Currency('PGK', u'', u'Kina')
currency_identifiers['PHP'] = Currency('PHP', u'₱', u'Philippine Peso')
currency_identifiers['PKR'] = Currency('PKR', u'₨', u'Pakistan Rupee')
currency_identifiers['PLN'] = Currency('PLN', u'zł', u'Zloty')
currency_identifiers['PYG'] = Currency('PYG', u'Gs', u'Guarani')
currency_identifiers['QAR'] = Currency('QAR', u'﷼', u'Qatari Rial')
currency_identifiers['RON'] = Currency('RON', u'lei', u'New Romanian Leu')
currency_identifiers['RSD'] = Currency('RSD', u'Дин.', u'Serbian Dinar')
currency_identifiers['RUB'] = Currency('RUB', u'руб', u'Russian Ruble')
currency_identifiers['RWF'] = Currency('RWF', u'', u'Rwanda Franc')
currency_identifiers['SAR'] = Currency('SAR', u'﷼', u'Saudi Riyal')
currency_identifiers['SBD'] = Currency('SBD', u'$', u'Solomon Islands Dollar')
currency_identifiers['SCR'] = Currency('SCR', u'₨', u'Seychelles Rupee')
currency_identifiers['SDG'] = Currency('SDG', u'', u'Sudanese Pound')
currency_identifiers['SEK'] = Currency('SEK', u'kr', u'Swedish Krona')
currency_identifiers['SGD'] = Currency('SGD', u'$', u'Singapore Dollar')
currency_identifiers['SHP'] = Currency('SHP', u'£', u'Saint Helena Pound')
currency_identifiers['SLL'] = Currency('SLL', u'', u'Leone')
currency_identifiers['SOS'] = Currency('SOS', u'S', u'Somali Shilling')
currency_identifiers['SRD'] = Currency('SRD', u'$', u'Surinam Dollar')
currency_identifiers['SSP'] = Currency('SSP', u'', u'South Sudanese Pound')
currency_identifiers['STD'] = Currency('STD', u'', u'Dobra')
currency_identifiers['SVC'] = Currency('SVC', u'$', u'El Salvador Colon')
currency_identifiers['SYP'] = Currency('SYP', u'£', u'Syrian Pound')
currency_identifiers['SZL'] = Currency('SZL', u'', u'Lilangeni')
currency_identifiers['THB'] = Currency('THB', u'฿', u'Baht')
currency_identifiers['TJS'] = Currency('TJS', u'', u'Somoni')
currency_identifiers['TMT'] = Currency('TMT', u'', u'Turkmenistan New Manat')
currency_identifiers['TND'] = Currency('TND', u'', u'Tunisian Dinar')
currency_identifiers['TOP'] = Currency('TOP', u'', u'Pa’anga')
currency_identifiers['TRY'] = Currency('TRY', u'TL', u'Turkish Lira')
currency_identifiers['TTD'] = Currency('TTD', u'TT$', u'Trinidad and Tobago Dollar')
currency_identifiers['TWD'] = Currency('TWD', u'NT$', u'New Taiwan Dollar')
currency_identifiers['TZS'] = Currency('TZS', u'', u'Tanzanian Shilling')
currency_identifiers['UAH'] = Currency('UAH', u'₴', u'Hryvnia')
currency_identifiers['UGX'] = Currency('UGX', u'', u'Uganda Shilling')
currency_identifiers['USD'] = Currency('USD', u'$', u'US Dollar')
currency_identifiers['USN'] = Currency('USN', u'$', u'US Dollar (Next day)')
currency_identifiers['USS'] = Currency('USS', u'$', u'US Dollar (Same day)')
currency_identifiers['UYI'] = Currency('UYI', u'', u'Uruguay Peso en Unidades Indexadas (URUIURUI)')
currency_identifiers['UYU'] = Currency('UYU', u'$U', u'Peso Uruguayo')
currency_identifiers['UZS'] = Currency('UZS', u'лв', u'Uzbekistan Sum')
currency_identifiers['VEF'] = Currency('VEF', u'Bs', u'Bolivar Fuerte')
currency_identifiers['VND'] = Currency('VND', u'₫', u'Dong')
currency_identifiers['VUV'] = Currency('VUV', u'', u'Vatu')
currency_identifiers['WST'] = Currency('WST', u'', u'Tala')
currency_identifiers['XAF'] = Currency('XAF', u'', u'CFA Franc BEAC')
currency_identifiers['XAG'] = Currency('XAG', u'', u'Silver')
currency_identifiers['XAU'] = Currency('XAU', u'', u'Gold')
currency_identifiers['XBA'] = Currency('XBA', u'', u'Bond Markets Unit European Composite Unit (EURCO)')
currency_identifiers['XBB'] = Currency('XBB', u'', u'Bond Markets Unit European Monetary Unit (E.M.U.-6)')
currency_identifiers['XBC'] = Currency('XBC', u'', u'Bond Markets Unit European Unit of Account 9 (E.U.A.-9)')
currency_identifiers['XBD'] = Currency('XBD', u'', u'Bond Markets Unit European Unit of Account 17 (E.U.A.-17)')
currency_identifiers['XCD'] = Currency('XCD', u'$', u'East Caribbean Dollar')
currency_identifiers['XDR'] = Currency('XDR', u'', u'SDR (Special Drawing Right)')
currency_identifiers['XFU'] = Currency('XFU', u'', u'UIC-Franc')
currency_identifiers['XOF'] = Currency('XOF', u'', u'CFA Franc BCEAO')
currency_identifiers['XPD'] = Currency('XPD', u'', u'Palladium')
currency_identifiers['XPF'] = Currency('XPF', u'', u'CFP Franc')
currency_identifiers['XPT'] = Currency('XPT', u'', u'Platinum')
currency_identifiers['XSU'] = Currency('XSU', u'', u'Sucre')
currency_identifiers['XUA'] = Currency('XUA', u'', u'ADB Unit of Account')
currency_identifiers['YER'] = Currency('YER', u'﷼', u'Yemeni Rial')
currency_identifiers['ZAR'] = Currency('ZAR', u'R', u'Rand')
currency_identifiers['ZMK'] = Currency('ZMK', u'', u'Zambian Kwacha')
currency_identifiers['ZWL'] = Currency('ZWL', u'', u'Zimbabwe Dollar')
