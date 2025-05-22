document.addEventListener('DOMContentLoaded', () => {
  // Получаем CSRF токен из куки
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie('csrftoken');
  const gallery = document.querySelector('.gallery');
  if (!gallery) return;

  gallery.querySelectorAll('.photo-card').forEach(card => {
    const photoId = card.dataset.id;
    const likeBtn = card.querySelector('.like-button');
    const likeCountSpan = likeBtn.querySelector('.like-count');

    likeBtn.addEventListener('click', async () => {
      try {
        const response = await fetch('/like-photo/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
          },
          body: new URLSearchParams({
            photo_id: photoId,
          }),
        });

        const data = await response.json();

        if (data.error) {
          alert(data.error);
          return;
        }

        // Обновляем число лайков
        likeCountSpan.textContent = data.total_likes;

        // Обновляем стиль кнопки в зависимости от того, лайк поставлен или снят
        if (data.liked) {
          likeBtn.classList.add('liked');
        } else {
          likeBtn.classList.remove('liked');
        }

      } catch (error) {
        alert('Ошибка при отправке лайка');
        console.error(error);
      }
    });
  });
});
