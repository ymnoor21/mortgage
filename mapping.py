from enum import Enum


class category(Enum):
    F30_1 = '30-Year Fixed'
    F30_2 = '30-Year Fixed'
    F30_3 = '30-Year Fixed'
    F30J_1 = '30-Year Fixed Jumbo'
    F30J_2 = '30-Year Fixed Jumbo'
    F30J_3 = '30-Year Fixed Jumbo'
    F30NOMI_1 = '30-Year Fixed - No mortgage insurance'
    F30NOMI_2 = '30-Year Fixed - No mortgage insurance'
    F30NOMI_3 = '30-Year Fixed - No mortgage insurance'
    F30JMI_1 = '30-Year Fixed Jumbo - No mortgage insurance'
    F30JMI_2 = '30-Year Fixed Jumbo - No mortgage insurance'
    F30JMI_3 = '30-Year Fixed Jumbo - No mortgage insurance'
    F30FHA_1 = '30-Year Fixed-Rate FHA'


class company(Enum):
    safecu = 'Safe Credit Union'
    wellsfargo = 'Wells Fargo'
    quickenloans = 'Quicken Loans Inc'
