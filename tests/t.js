
/* changing title, adding name, and removing name
   all work as follows:
    - after the user inputs a string to change the title, add a name,
      or remove a name, the backend handles testing the constraints of
      that input and updates the object accordingly.
    - the frontend then receives the new Tune object and a boolean as to whether
      the Tune object was updated (ie if the input matches the constraints or if
      the update was a failure).
    - the frontend uses the functions changeHTML<...> with the boolean to then update
      the html text boxes. these tests are just testing whether the pages display the
      correct tune titles or names after changeHTMLTuneTitle is called with either the
      true or false input
 */

describe("changing title", function() {
  beforeEach(function() {
    setUpHTMLFixture();
  });

  changeHTMLTuneTitle(true); // takes a boolean isSuccess based on if the change was successful or not (ie does new title fit constraints?)
                             // the title is changed if isSuccess is true

  it("valid title change renders in html", function() {
    expect($('#tuneTitle').toHaveText(getTuneTitle())); // getTuneTitle() will be a function that returns the tune title from the backend's response after updating the Tune object
  });

  changeHTMLTuneTitle(false);

  it("invalid title change does not change html", function() {
    expect($('#tuneTitle').toHaveText(getTuneTitle())); // the title should still match the tune object's title
  });
});

describe("adding name", function() {
  beforeEach(function() {
    setUpHTMLFixture();
  });

  changeHTMLName(true); // takes a boolean isSuccess based on if the change was successful or not (ie does new name fit constraints?)
                         // the name is added if isSuccess is true

  it("valid name change renders in html", function() {
    expect($('#names').toHaveText(getTuneContributors()));
  });

  changeHTMLName(false);

  it("invalid name change does not change html", function() {
    expect($('#names').toHaveText(getTuneContributors())); // the names should still match the tune object's contributors
  });

});

describe("removing name", function() {
  beforeEach(function() {
    setUpHTMLFixture();
  });

  changeHTMLName(true); // takes a boolean isSuccess based on if the deletion was successful or not (ie was the name the user wanted to delete actually present?)
                         // the name is removed if isSuccess is true

  it("valid name change renders in html", function() {
    expect($('#names').toHaveText(getTuneContributors()));
  });

  changeHTMLName(false);

  it("invalid name change does not change html", function() {
    expect($('#names').toHaveText(getTuneContributors())); // the names should still match the tune object's contributors
  });
});


describe("uploading midi", function() {
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


describe("downloading pdf", function() {

  var eventListener = {};
  fakeFile = {name : "test.pdf"};

  beforeEach(function() {
      setUpHTMLFixture();

  });

  displayHTMLTune(true); // takes a boolean isSuccess

  it("tune file successfully uploaded", function() {
    expect($('#tuneTitle').not.toBeNull());
  });

  displayHTMLTune(true);

  it("invalid title change", function() {
    expect($('#tuneTitle').not.toBeNull());
  });


});