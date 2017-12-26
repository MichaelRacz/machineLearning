Feature: As consumer of the datastore
  I want a distributed log of create and
  delete operations.

  Scenario: Log the creation of a wine record
    Given I have a valid wine record
    When I POST it to the create_wine endpoint
    Then the creation is logged

  Scenario: Log the deletion of a wine record
    Given I have a valid wine record
      And I POST it to the create_wine endpoint
    When I DELETE the record
    Then the deletion is logged
