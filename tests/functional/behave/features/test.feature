Feature: showing off cli-bdd

    Scenario: login with CLI
        Given a file "/tmp/login.py" with:
            """
            login = input('Login: ')
            password = input('Password: ')
            print('Welcome {}!'.format(login))
            print('Your password is "{}"'.format(password))
            """
        When I run `python /tmp/login.py` interactively
        And I got "Login: " for interactive dialog
        And I type "root"
        And I got "Password: " for interactive dialog
        And I type "123456"
        Then the output should contain exactly:
            """
            Welcome root!
            Your password is "123456"

            """
