function searchTable() {
  const input = document.getElementById('searchInput');
  const filter = input.value.toLowerCase();
  const table = document.getElementById('dataTable');
  const rows = table.getElementsByTagName('tr');

  for (let i = 1; i < rows.length; i++) {
      const cells = rows[i].getElementsByTagName('td');
      let match = false;

      for (let j = 0; j < cells.length; j++) {
          const originalText = cells[j].getAttribute('data-original-text') || cells[j].innerText;

          if (!cells[j].hasAttribute('data-original-text')) {
              cells[j].setAttribute('data-original-text', originalText);
          }

          cells[j].innerText = originalText;

          if (originalText.toLowerCase().includes(filter)) {
              match = true;

              const regex = new RegExp(`(${filter})`, 'gi');
              cells[j].innerHTML = originalText.replace(regex, '<span class="highlight-dashboard">$1</span>');
          }
      }

      rows[i].style.display = match ? '' : 'none';
  }
}
