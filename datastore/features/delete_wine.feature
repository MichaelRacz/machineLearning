Feature: As a maintainer of the wine dataset
  I want to delete wine records of the dataset.

  Background:
    Given I have access to the Wine API
      And I have a valid wine record
      And I POST it to the create_wine endpoint

  Scenario: Delete a wine record
    When I DELETE the record
    Then the HTTP status code is "204"

  Scenario: Retrieve a deleted wine record
    When I DELETE the record
      And I GET the record from the get_wine endpoint
    Then I receive an error indicating that there is no record with the given id

  Scenario: Delete an unknown id
    When I DELETE a record with the id "54321"
    Then I receive an error indicating that there is no record with the given id
      And the HTTP status code is "404"

  Scenario: Delete a malformed id
    When I DELETE a record with the id "malformed"
    Then I receive an error indicating that the id is malformed
      And the HTTP status code is "400"
