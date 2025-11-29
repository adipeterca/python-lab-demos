import json

result_dict = {
    "test_logs" : [],
    "errors" : [],
    "score" : 0
}

def test_problem1() -> tuple[int, list[str]]:
    '''
    Here goes the description for the problem, if it is not present on the website.
    '''

    test_passed = 0
    output = []

    try:
        result = uc.problem1(10, 20)
        assert(result == 30)
        test_passed += 1
    except Exception as e:
        output.append(f":x: Problem 1 - Test 1 : failed\nReason: `{e}`\n")
    
    return test_passed, output


if __name__ == "__main__":
    try:
        # If the student submitted invalid Python code, this will throw an error
        import usercode as uc

        test_passed, output = test_problem1()
        result_dict["score"] += test_passed
        result_dict["test_logs"] += output
            
    except NameError as e:
        result_dict["test_logs"].append(f":x: Testing failed\nReason: `{e}`\n")
    
    except Exception as e:
        result_dict["errors"].append(str(e))
    
    finally:
        print("JSON-DELIMITER")
        print(json.dumps(result_dict))