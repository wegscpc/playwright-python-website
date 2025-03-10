Feature: Google Search Functionality
  As a user
  I want to search on Google
  So that I can find relevant information

  Background:
    Given I am on the search page

  @smoke
  Scenario: Basic search functionality
    When I enter "playwright testing" in the search box
    And I click the search button
    Then I should see search results
    And the first result should contain "playwright"
    And the page title should contain "playwright testing"

  @regression
  Scenario Outline: Search with different inputs
    When I enter "<search_text>" in the search box
    And I click the search button
    Then I should see search results
    And the first result should contain "<expected_text>"

    Examples:
      | search_text      | expected_text |
      | playwright test  | playwright    |
      | python testing   | python        |
      | web automation   | automation    |
