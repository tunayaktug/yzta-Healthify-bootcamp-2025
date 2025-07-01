document.getElementById('categoryDropdown').addEventListener('change', function() {
  const selected = this.value;
  if (selected !== "Kategori Seçin") {
    window.location.href = `/upload.html?category=${selected}`;
  }
});

const testimonials = [
  {
    name: "Sarah W.",
    photo: "https://randomuser.me/api/portraits/women/44.jpg",
    comment: "“Harika bir araç! Sağlık yönetimimde bana çok yardımcı oldu.”"
  },
  {
    name: "Ali K.",
    photo: "https://randomuser.me/api/portraits/men/34.jpg",
    comment: "“Çok hızlı ve kullanışlı bir sistem. Kesinlikle öneririm.”"
  },
  {
    name: "Elif T.",
    photo: "https://randomuser.me/api/portraits/women/68.jpg",
    comment: "“Yapay zeka analizi gerçekten etkileyici.”"
  },
  {
    name: "Deniz A.",
    photo: "https://randomuser.me/api/portraits/men/23.jpg",
    comment: "“Görsel yükledikten birkaç saniye sonra net bilgi aldım.”"
  },
  {
    name: "Zeynep B.",
    photo: "https://randomuser.me/api/portraits/women/25.jpg",
    comment: "“Kullanıcı dostu arayüzü çok beğendim.”"
  }
];

let currentIndex = 0;

function showTestimonial(index) {
  currentIndex = index;
  const testimonial = testimonials[index];
  document.querySelector('.user-photo').src = testimonial.photo;
  document.getElementById('userName').textContent = testimonial.name;
  document.getElementById('userComment').textContent = testimonial.comment;

  // Dots
  document.querySelectorAll('.dot').forEach(dot => dot.classList.remove('active'));
  document.querySelectorAll('.dot')[index].classList.add('active');
}

// Otomatik geçiş (opsiyonel)
setInterval(() => {
  currentIndex = (currentIndex + 1) % testimonials.length;
  showTestimonial(currentIndex);
}, 6000); // Her 6 saniyede değişir

document.getElementById('loginBtn').addEventListener('click', function () {
  window.location.href = "login.html";
});
// İlk yükleme
showTestimonial(0);

document.addEventListener("DOMContentLoaded", () => {
  const newsSection   = document.getElementById('news-section');
  const newsContainer = document.getElementById('news-container');

  // Türkçe sağlık haberleri için RSS beslemesi
  const RSS_URL   = 'https://www.sabah.com.tr/rss/saglik.xml';
  const PROXY_URL = 'https://api.allorigins.win/raw?url=' + encodeURIComponent(RSS_URL);

  // Karıştırma fonksiyonu
  function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
  }

  // Önceki/Sonraki butonları
  const prevBtn = document.createElement('button');
  prevBtn.className = 'news-nav prev';
  prevBtn.textContent = '‹';
  const nextBtn = document.createElement('button');
  nextBtn.className = 'news-nav next';
  nextBtn.textContent = '›';
  newsSection.append(prevBtn, nextBtn);

  prevBtn.addEventListener('click', () => {
    newsContainer.scrollBy({ left: -newsContainer.clientWidth * 0.8, behavior: 'smooth' });
  });
  nextBtn.addEventListener('click', () => {
    newsContainer.scrollBy({ left:  newsContainer.clientWidth * 0.8, behavior: 'smooth' });
  });

  // RSS’i çek, karıştır, ilk 10’u göster
  fetch(PROXY_URL)
    .then(res => {
      if (!res.ok) throw new Error('Ağ hatası');
      return res.text();
    })
    .then(str => new window.DOMParser().parseFromString(str, 'text/xml'))
    .then(data => {
      const items = Array.from(data.querySelectorAll('item'));
      shuffle(items);
      items.slice(0, 10).forEach(item => {
        const title = item.querySelector('title')?.textContent || '';
        const link  = item.querySelector('link')?.textContent  || '#';
        let   desc  = item.querySelector('description')?.textContent || '';
        desc = desc.replace(/<[^>]+>/g, '').slice(0, 100) + '…';

        // Görsel URL’si
        let imgUrl = 'https://via.placeholder.com/300x180?text=Resim+Yok';
        const thumb = item.querySelector('media\\:thumbnail, thumbnail');
        const enc   = item.querySelector('enclosure');
        if (thumb?.getAttribute('url'))    imgUrl = thumb.getAttribute('url');
        else if (enc?.getAttribute('url')) imgUrl = enc.getAttribute('url');

        // Kart oluştur
        const card = document.createElement('a');
        card.href      = link;
        card.target    = '_blank';
        card.className = 'news-card';
        card.innerHTML = `
          <img src="${imgUrl}" alt="${title}">
          <div class="news-card-content">
            <h3>${title}</h3>
            <p>${desc}</p>
          </div>
        `;
        newsContainer.append(card);
      });
    })
    .catch(err => {
      console.error(err);
      newsContainer.innerHTML = '<p>Haberler yüklenemedi.</p>';
    });
});
