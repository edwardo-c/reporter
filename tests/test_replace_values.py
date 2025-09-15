from plan_executor.operations import value_map as vm
import pandas as pd

def test_replace_values():
    
    df = pd.DataFrame(
        {'col_A': ['keep', 'replace', 'keep'],
         'col_B': ['keep', 'replace', 'keep']})
    
    value_map = {
        'col_A': {'replace': 'REPLACED'},
        'col_B': {'replace': 'REPLACED'}}
   
    expected = pd.DataFrame(
        {'col_A': ['keep', 'REPLACED', 'keep'],
         'col_B': ['keep', 'REPLACED', 'keep']})

    result = vm.replace_values(df=df,value_map=value_map, case_insensitive=False)

    pd.testing.assert_frame_equal(result, expected)


def test_replace_values_insensitive():
    
    df = pd.DataFrame(
        {'col_A': ['keep', 'Replace', 'keep'],
         'col_B': ['keep', 'rePLACE', 'keep']})
    
    value_map = {
        'col_A': {'rEplace': 'REPLACED'},
        'col_B': {'replAce': 'REPLACED'}}
   
    expected = pd.DataFrame(
        {'col_A': ['keep', 'REPLACED', 'keep'],
         'col_B': ['keep', 'REPLACED', 'keep']})

    result = vm.replace_values(df=df,value_map=value_map, case_insensitive=True)

    pd.testing.assert_frame_equal(result, expected)