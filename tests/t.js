describe("A suite", function() {
  it("contains spec with an expectation", function() {
    expect(true).toBe(true);
  });
});

// outline of tests

describe("changing title", function()) {
  beforeEach(funtion() {
    setUpHTMLFixture();
  });

  changeHTMLTuneTitle(true); // takes a boolean isSuccess

  it("valid title change", function()) {
    expect($('#tuneTitle').toHaveText(getTuneTitle()));
  });

  changeHTMLTuneTitle(false);
  it("invalid title change", function()) {
    expect($('#tuneTitle').toHaveText(getTuneTitle()));

  }
});