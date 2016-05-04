describe("A suite", function() {
  it("contains spec with an expectation", function() {
    expect(true).toBe(true);
  });
});

// outline of tests

describe("changing title", function()) {
  beforeEach(function() {
    setUpHTMLFixture();
  });

  changeHTMLTuneTitle(true); // takes a boolean isSuccess

  it("valid title change", function() {
    expect($('#tuneTitle').toHaveText(getTuneTitle()));
  });

  changeHTMLTuneTitle(false);
  it("invalid title change", function()) {
    expect($('#tuneTitle').toHaveText(getTuneTitle()));

  }
});


describe("uploading midi", function()) {
  // uses some code from https://www.noppanit.com/javascript-tdd-on-file-upload/
  // this post was helpful as well http://stackoverflow.com/questions/4234589/validation-of-file-extension-before-uploading-file
  var eventListener = {};
  var badFile = {name : "bad.png"};
  var goodFile = {name : "good.midi"}

  spyOn($, "ajax");
  eventListener = jasmine.createSpy();
  spyOn(window, "FileReader").andReturn({
    addEventListener: eventListener,
    readAsDataURL : function(file) {
      // do nothing.
    }
  });

  uploader = new Uploader(badFile);    // an Uploader function to be defined in our page

  it("should not upload file", function() {
    thumbnailElement = $("<div></div>");
    uploader.upload({
      progressbar : function() {

      },
      thumbnailDiv : thumbnailElement
    });

    expect(eventListener.mostRecentCall.args[0]).toEqual('load');

    eventListener.mostRecentCall.args[1]({
      target : {
        result : 'file content'
      }
    });

    expect($.ajax.mostRecentCall.args[0]["url"]).toEqual("/upload/file");
    expect($.ajax.mostRecentCall.args[0]["type"]).toEqual("POST");
    expect($('#midi-file')).toBeNull();
  });


  uploader = new Uploader(goodFile);    // an Uploader function to be defined in our page

  it("should upload a file successfully", function() {
    thumbnailElement = $("<div></div>");
    uploader.upload({
      progressbar : function() {

      },
      thumbnailDiv : thumbnailElement
    });

    expect(eventListener.mostRecentCall.args[0]).toEqual('load');

    eventListener.mostRecentCall.args[1]({
      target : {
        result : 'file content'
      }
    });

    expect($.ajax.mostRecentCall.args[0]["url"]).toEqual("/upload/file");
    expect($.ajax.mostRecentCall.args[0]["type"]).toEqual("POST");
    expect($('#midi-file')).not.toBeNull();
  });

});


describe("downloading pdf", function()) {

  var eventListener = {};
  fakeFile = {name : "test.pdf"};

  beforeEach(function() {
      setUpHTMLFixture();

  });

  displayHTMLTune(true); // takes a boolean isSuccess

  it("tune file successfully uploaded", function() {
    expect($('#tuneTitle').not.toBeNull();
  });

  displayHTMLTune(true);

  it("invalid title change", function()) {
    expect($('#tuneTitle').not.toBeNull();
  }


});