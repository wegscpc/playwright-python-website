Feature: Google Search
    As a user
    I want to search on Google
    So that I can find relevant information

    Background:
        Given I am on the Google search page
        And I handle the consent dialog if present

    Scenario: Perform a basic search
        When I search for "playwright python testing"
        Then I should see search results
        And the results should contain "Playwright"

    Scenario: Search with special characters
        When I search for "playwright + python automation"
        Then I should see search results
        And the results should contain "automation"

    @skip_captcha
    Scenario: Handle CAPTCHA detection
        When I perform multiple searches
        Then I should handle CAPTCHA detection gracefully
        And I should log appropriate warnings
