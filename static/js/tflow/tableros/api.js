document.querySelectorAll('form[data-api-method]').forEach((form) => {
  const ownerField = form.querySelector('[name="usuario"]');
  if (form.dataset.apiMethod === 'PATCH' && ownerField) {
    ownerField.disabled = true;
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const feedback = form.querySelector('[data-api-feedback]');
    const submitButton = form.querySelector('[type="submit"]');
    const headers = {
      Accept: 'application/json',
      'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value,
    };
    const options = {
      method: form.dataset.apiMethod,
      headers,
      credentials: 'same-origin',
    };

    if (options.method === 'PATCH') {
      const payload = {};
      new FormData(form).forEach((value, key) => {
        if (key !== 'csrfmiddlewaretoken') {
          payload[key] = value;
        }
      });
      headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(payload);
    }

    submitButton.disabled = true;
    feedback.hidden = true;

    try {
      const response = await fetch(form.dataset.apiUrl, options);
      if (!response.ok) {
        const errors = await response.json();
        feedback.textContent = Object.entries(errors)
          .map(([field, messages]) => `${field}: ${messages}`)
          .join(' ');
        feedback.hidden = false;
        return;
      }

      window.location.assign(form.dataset.successUrl);
    } catch (error) {
      console.error(`No se pudo completar ${options.method}:`, error);
      feedback.textContent = 'No se pudo completar la solicitud. Intenta nuevamente.';
      feedback.hidden = false;
    } finally {
      submitButton.disabled = false;
    }
  });
});
