Feature: As a maintainer of the wine dataset
  I want to create new wine records and add
  them to the dataset.

  Background:
    Given I have access to the Wine API

  Scenario: Create a new wine record
    Given I have a valid wine record
    When I POST it to the create_wine endpoint
    Then I receive the id of created wine record
      And I GET the record from the get_wine endpoint
