from functions.run_python_file import run_python_file

def main():
    # Test 1: Run main.py without args (should print usage or default output)
    print("TEST 1:")
    print(run_python_file("calculator", "main.py"))
    print("\n----------------------\n")

    # Test 2: Run main.py with arguments
    print("TEST 2:")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("\n----------------------\n")

    # Test 3: Run tests file (should execute tests successfully)
    print("TEST 3:")
    print(run_python_file("calculator", "tests.py"))
    print("\n----------------------\n")

    # Test 4: Path traversal attempt (should fail)
    print("TEST 4:")
    print(run_python_file("calculator", "../main.py"))
    print("\n----------------------\n")

    # Test 5: Non-existent file
    print("TEST 5:")
    print(run_python_file("calculator", "nonexistent.py"))
    print("\n----------------------\n")

    # Test 6: Wrong file type (not .py)
    print("TEST 6:")
    print(run_python_file("calculator", "lorem.txt"))
    print("\n----------------------\n")


if __name__ == "__main__":
    main()