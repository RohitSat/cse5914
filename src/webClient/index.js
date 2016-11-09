// No framework makes for a sloppy js file :(

const baseURL = 'http://localhost:5000';

// speech recognition
var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
var recognition = new SpeechRecognition();
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

// UI stuff
const textInput = document.querySelector('#textInput');
const submitButton = document.querySelector('#submitButton');
const micButton = document.querySelector('#micButton');
const outputBox = document.querySelector('.output');
const buttonStates = {
  ready: () => {
    writeToBox('Submit a query', submitButton);
  },
  submitting: () => {
    writeToBox('Submitting...', submitButton);
  },
  processing: () => {
    writeToBox('Processing...', submitButton);
  },
};
document.addEventListener('DOMContentLoaded', buttonStates.ready);
/**
 * "Says" a thing out loud using the speechSynthesis api
 * @param  {string} thing thing to say out loud
 */
const sayThing = (thing) => {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(thing);
  synth.speak(utterance);
};

submitButton.addEventListener('click', (e) => {
  const val = textInput.value;
  writeToBox('Processing: ' + val, outputBox);
  submitButton.innerHTML = 'Sending Query...';
  postQuery(val);
});

/**
 * updates the content value of a DOM node
 * @param {string} value node value
 */
const setNodeValue = (node, value) => {
  var tag = node.tagName.toLowerCase();
  if (tag == 'textarea') {
    node.value = value;
  }
  else {
    node.innerHTML = value;
  }
};

/**
 * writes to a given dom node's innerhtml using a cool typing style.
 * @param  {string} text       the output text to be rendered
 * @param  {Number} [time=500] the total time the whole typing should take
 */
const writeToBox = (text, box, time = 500) => {
  setNodeValue(box, '');
  const timeout = time / text.length;
  let counter = 0;

  const interval = setInterval(
    () => {
      if (counter++ > text.length) {
        clearInterval(interval);
      } else {
        setNodeValue(box, text.substring(0, counter));
      }
    },
    timeout
  );
};

/**
 * Sends an HTTP post request to a hard-coded url entailing the query in its body
 * @param  {string} query  user's query
 * @return {Promise}       promise returned from fetch
 */
const postQuery = (query) => {
  const queryRequestSettings = {
    method: 'POST',
    headers: new Headers({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ text: query }),
  };
  fetch(baseURL + '/api/request', queryRequestSettings)
    .then(res => {
      if (res.ok) {
        return res;
      }
      throw new Error('Error with posting query');
    })
    .then(res => res.json())
    .then(obj => obj.id)
    .then(startPolling)
    .catch(console.log);
};

/**
 * polls a hard-coded url with a give jobID
 * @param  {string} jobID  id of the job to poll for
 * @return {[type]}       [description]
 */
const startPolling = (jobID) => {
  buttonStates.processing();
  const timeout = 1000;
  const poll = () => {
    fetch(`${baseURL}/api/request/${jobID}`)
      .then(res => {
        if (res.ok) {
          return res;
        }
        throw new Error('Error polling for response, id:', jobID);
      })
      .then(res => res.json())
      .then(obj => {
        if (obj.status === 'finished') {
          buttonStates.ready();
          writeToBox(obj.output.text, outputBox);
          sayThing(obj.output.text);
        } else if (obj.status === 'queued' || obj.status === 'started') {
          //buttonStates.processing();
          setTimeout(poll(), timeout);
        } else if (obj.status === 'failed') {
          writeToBox('Request failed at processing stage', outputBox);
          buttonStates.ready();
        }
      })
      .catch(console.log);
  };

  setTimeout(poll(), timeout);
}

const startListening = (e) => {
  e.target.removeEventListener(e.type, startListening);
  recognition.start();
  console.log('listening...');
  micButton.style.backgroundColor = 'red';
  micButton.innerHTML = 'Listening';
}
micButton.addEventListener('click', startListening);

recognition.onresult = e => {
  const { confidence, transcript } = e.results[0][0];
  console.log(`Speech was parsed to ${transcript} with confidence of ${confidence}`);
  if (confidence > .3) {
    writeToBox(transcript, textInput);
  }
};

recognition.onspeechend = () => {
  recognition.stop();
  console.log('stopped listening');
  micButton.style.backgroundColor = '';
  micButton.addEventListener('click', startListening);
  micButton.innerHTML = 'Mic';
};
