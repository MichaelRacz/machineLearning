Feature: As a user of the classification API
  I want to classify wines using the Nearest Neighbor algorithm

  @needs_state_reset
  Scenario: Classify using the Nearest Neighbor algorithm
    Given the datastore contains a training set
    When I classify the test set using the Nearest Neighbor algorithm
    Then the test set is classified correctly, regarding suitable tolerance
