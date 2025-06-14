document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.curtir-form').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const postId = form.dataset.postId;
      const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

      fetch(form.action, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken
        },
        body: new URLSearchParams({
          post_id: postId
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.curtido !== undefined) {
          const btn = form.querySelector('.curtir-btn');
          const contador = form.querySelector('.contador-curtidas');

          btn.innerHTML = data.curtido ? '❤️' : '🤍';
          contador.innerText = data.total_curtidas;
        }
      });
    });
  });
});
