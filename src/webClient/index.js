const baseURL = 'http://localhost:5000';

const textInput = document.querySelector('#textInput');
const submitButton = document.querySelector('#submitButton');
const outputBox = document.querySelector('.output');
const buttonStates = {
  ready: () => {
    writeToBox('Submit a query', submitButton);
    submitButton.className = "ready";
  },
  submitting: () => {
    writeToBox('Submitting...', submitButton);
    submitButton.className = "submitting";
  },
  processing: () => {
    writeToBox('Processing...', submitButton);
    submitButton.className = 'processing';
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
  const engVoice = synth.getVoices()[3];
  utterance.voice = engVoice;
  synth.speak(utterance);
};

submitButton.addEventListener('click', (e) => {
  const val = textInput.value;
  writeToBox('Processing:' + val, outputBox);
  submitButton.innerHTML = 'Sending Query...';
  postQuery(val);
});

/**
 * writes to div.output using a cool typing style.
 * @param  {string} text       the output text to be rendered
 * @param  {Number} [time=500] the total time the whole typing should take
 */
const writeToBox = (text, box, time = 500) => {
  box.innerHTML = '';
  const timeout = time / text.length;
  let counter = 0;

  const interval = setInterval(
    () => {
      if (counter++ > text.length) {
        clearInterval(interval);
      } else {
        box.innerHTML = text.substring(0, counter);
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
  const headers = new Headers();
  headers.append('content-type', 'application/json');
  console.log(headers.get('content-type'));
  const queryRequestSettings = {
    method: 'POST',
    mode: 'no-cors',
    headers: headers,
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
    .then(res => {
      console.log(res);
      return res;
    })
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
  const timeout = 1000;
  const poll = () => {
    fetch(`${baseURL}/api/${jobID}`)
      .then(res => {
        if (res.ok) return res;
        throw new Error('Error polling for response, id:', jobID)
      })
      .then(res => res.json())
      .then(obj => {
        if (obj.status === 'complete') {
          writeToOutputBox(obj.output.text);
        } else if (obj.status === 'queued') {
          setTimeout(poll(), timeout);
        }
      })
      .catch(console.log);
  };

  const timeoutClear = setTimeout(poll(), timeout);
}
