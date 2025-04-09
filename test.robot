*** Settings ***
Library    BuiltIn

*** Test Cases ***
Test BuiltIn
    [Documentation]    Test listener for BuiltIn keywords
    ${var_1}=    Set Variable    ${5}
    FOR    ${counter}    IN RANGE    ${1}    ${5}
        Log    var_1 : ${var_1}
        ${var_1}=    Set Variable    ${var_1 - 1}
    END