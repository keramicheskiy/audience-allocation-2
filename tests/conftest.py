def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.write_line("\n=== PASSED TESTS ===")
    for rep in terminalreporter.getreports("passed"):
        terminalreporter.write_line(f"{rep.nodeid}: PASSED")

    terminalreporter.write_line("\n=== FAILED/ERROR TESTS ===")
    for rep in terminalreporter.getreports("failed") + terminalreporter.getreports("error"):
        terminalreporter.write_line(f"{rep.nodeid}: {rep.outcome.upper()}")
