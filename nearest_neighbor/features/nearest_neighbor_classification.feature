Feature: As a user of the nearest neighbor service
  I want to classify wines using the Nearest Neighbor algorithm

  Scenario: Classify using the Nearest Neighbor algorithm
    Given the nearest neighbor service is initialized with a training set
    When I classify the test set using the Nearest Neighbor algorithm
    Then the test set is classified correctly, regarding suitable tolerance
