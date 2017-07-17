Feature: As a maintainer of the wine dataset
  I want to retrieve wine records of the dataset.

  Background:
    Given I have a valid wine record
      And I POST it to the create_wine endpoint

  Scenario: Receive a wine record
    When I GET the record from the get_wine endpoint
    Then the HTTP status code is "200"

  Scenario: Pass an unknown id
    When I GET a record with the id "54321"
    Then I receive an error indicating that there is no record with the given id
      And the HTTP status code is "404"

  Scenario: Pass a malformed id
    When I GET a record with the id "malformed"
    Then I receive an error indicating that the id is malformed
      And the HTTP status code is "400"
