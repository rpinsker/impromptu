
/* test for parsing json file in javascript using json file with the following:
*
  {
    "tune": {
        "timeSignature": ["3","4"],
        "clef": "0",
        "title":"tune title!",
        "contributors": ["contributor one","contributor two"],
		"notes": [
          {
            "duration": "0",
            "frequency": "25.0",
            "onset": "5.67",
            "pitch": {
              "letter": "b",
              "octave": "2",
              "accidental": "2",
            }
          },
          {
            "duration": "3",
            "frequency": "105.0",
            "onset": "23.93",
            "pitch": {
              "letter": "r",
              "octave": "5",
              "accidental": "1",
            }
          }
        ],
        keySignature: {
          "isMajor":"true",
          "pitch": {
            "letter":"b",
            "octave":"2",
            "accidental":"2",
          }
        }
    }
  }
*
* */
describe ("parse json", function() {
    beforeEach(function() {
    parseJSON(tune.json); // parses the json file and stores the info accordingly
  });

  it("json parsing", function() {
    expect(getTuneTitle()).toEqual("tune title!");
    expect(getClef()).toEqual(0);
    expect(getContributors).toEqual(["contributor one","contributor 2"]);
    expect(length(getNotes())).toEqual(2);
    expect(getLetter(getPitch(getKeySignature()))).toEqual("b");
  });

});

/* changing title, adding name, and removing name
   all work as follows:
    - after the user inputs a string to change the title, add a name,
      or remove a name, the backend handles testing the constraints of
      that input and updates the object accordingly.
    - the frontend then receives the new Tune object (as a JSON file) and a boolean as to whether
      the Tune object was updated (ie if the input matches the constraints or if
      the update was a failure).
    - the frontend uses the functions changeHTML<...> with the boolean to then update
      the html text boxes if necessary. these tests are just testing whether the pages display the
      correct tune titles or names after changeHTMLTuneTitle is called with either the
      true or false input
 */

describe("changing title", function() {
  beforeEach(function() {
    setUpHTMLFixture();
    parseJSON(tune.json); // parses the json file and stores the info accordingly in variables
                          // that can be set and retrieved from the javascript files
  });


  it("valid title change renders in html", function() {
    setTuneTitle("good title");
    changeHTMLTuneTitle(true); // takes a boolean isSuccess based on if the change was successful or not (ie does new title fit constraints?)
                               // the title is changed if isSuccess is true.
    expect($('#tuneTitle').toHaveText("good title")); // getTuneTitle() will be a function that returns the tune title from the backend's response after updating the Tune object
  });

  it("invalid title change does not change html", function() {
    setTuneTitle("good title");
    changeHTMLTuneTitle(false);
    expect($('#tuneTitle').toHaveText("tune title!")); // the title should not have changed from the original JSON file
                                                       // even though setTuneTitle changed the title because false was sent to changeHTMLTuneTitle
  });
});

describe("adding name", function() {
  beforeEach(function() {
    setUpHTMLFixture();
    parseJSON(tune.json); // parses the json file and stores the info accordingly in variables
                          // that can be set and retrieved from the javascript files
  });

  it("valid name change renders in html", function() {
    addName("contributor three");
    changeHTMLName(true); // takes a boolean isSuccess based on if the change was successful or not (ie does new name fit constraints?)
                          // the name is added if isSuccess is true
    expect($('#names').toHaveText("contributor one, contributor two, contributor three"));
  });



  it("invalid name change does not change html", function() {
    addName("contributor three");
    changeHTMLName(false);
    expect($('#names').toHaveText("contributor one, contributor two")); // the names should still match the original contributors according to the JSON file
  });

});

describe("removing name", function() {
  beforeEach(function() {
    setUpHTMLFixture();
    parseJSON(tune.json); // parses the json file and stores the info accordingly in variables
                          // that can be set and retrieved from the javascript files
  });


  it("valid name change renders in html", function() {
    removeName("contributor one")
    changeHTMLName(true); // takes a boolean isSuccess based on if the deletion was successful or not (ie was the name the user wanted to delete actually present?)
                          // the name is removed if isSuccess is true
    expect($('#names').toHaveText("contributor two"));
  });

  it("invalid name change does not change html", function() {
    // user tries removing a non-existent name
    changeHTMLName(false);
    expect($('#names').toHaveText("contributor one, contributor two")); // the names should still match the contributors according to the JSON file
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