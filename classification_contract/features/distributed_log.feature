Feature: As user of the classification contract
  I want a distributed log of create/delete
  wine messages.

  Scenario: Log the creation of a wine record
    Given I have a classified wine
    When I POST it to the wines endpoint
    Then the creation is logged

  Scenario: Log the deletion of a wine record
    Given I have a classified wine
      And I POST it to the wines endpoint
    When I DELETE the record
    Then the deletion is logged
