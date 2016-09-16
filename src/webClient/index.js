const textInput = document.querySelector('#textInput');
const submitButton = document.querySelector('#submitButton');

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
}

submitButton.addEventListener('click', (e) => {
  writeToOutputBox('Processing:', e.target.value);
  postQuery(e.target.value);
});

/**
 * writes to div.output using a cool typing style.
 * @param  {string} text       the output text to be rendered
 * @param  {Number} [time=500] the total time the whole typing should take
 */
const writeToOutputBox = (text, time = 500) => {
  const output = document.querySelector('.output');
  output.innerHTML = '';
  const timeout = time / text.length;
  let counter = 0;

  const interval = setInterval(
    () => {
      if (counter++ > text.length) {
        clearInterval(interval);
      } else {
        output.innerHTML = text.substring(0, counter);
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
  const url = 'http://requestb.in/1e0i6cq1';
  const queryRequestSettings = {
    body: 'query=' + encodeURIComponent(query),
  };
  const fails = 0;
  fetch(url, queryRequestSettings)
    .then(res => res.ok ? res : throw new Error('Error with posting query'))
    .then(res => res.json())
    .then(obj => obj.jobID)
    .then(startPolling)
    .catch(er => {
      console.log(er);
      if (fails++ < 3) {
        postQuery(query);
      }
    });
};

/**
 * polls a hard-coded url with a give jobID
 * @param  {string} jobID  id of the job to poll for
 * @return {[type]}       [description]
 */
const startPolling = (jobID) => {
  const url = `sampleURL${jobID}`;
  const timeout = 1000;
  const fails = 0;
  const poll = () => {
    fetch(url)
      .then(res => res.ok ? res : throw new Error('Error polling for response, jobID:', jobID))
      .then(res => res.json())
      .then(obj => {
        if (obj.status === 'complete') {
          writeToOutputBox(obj.output.text);
        } else if (obj.status === 'processing') {
          setTimeout(poll(), timeout);
        }
      })
      .catch(er => {
        console.log(er);
        if (fails++ < 3) {
          setTimeout(poll(), timeout);
        }
      });
  };

  const timeoutClear = setTimeout(poll(), timeout)    ;
}
