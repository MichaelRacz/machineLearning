Feature: As an operator of the datastore
  I want the datastore to set its state by
  reading all entries of the distributed log
  and applying them.

  @needs_state_reset
  Scenario: Apply existing log entries
    Given I have some create and delete entries logged
    When the datastore is synchronized
    Then the create entries can be received
      And the delete entries cannot be received
