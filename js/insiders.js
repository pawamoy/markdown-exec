function humanReadableAmount(amount) {
    const strAmount = String(amount);
    if (strAmount.length >= 4) {
        return `${strAmount.slice(0, strAmount.length - 3)},${strAmount.slice(-3)}`;
    }
    return strAmount;
}

function getJSON(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function () {
        var status = xhr.status;
        if (status === 200) {
            callback(null, xhr.response);
        } else {
            callback(status, xhr.response);
        }
    };
    xhr.send();
}

function updateInsidersPage(author_username) {
    const sponsorURL = `https://github.com/sponsors/${author_username}`
    const dataURL = `https://raw.githubusercontent.com/${author_username}/sponsors/main`;
    getJSON(dataURL + '/numbers.json', function (err, numbers) {
        document.getElementById('sponsors-count').innerHTML = numbers.count;
        Array.from(document.getElementsByClassName('sponsors-total')).forEach(function (element) {
            element.innerHTML = '$ ' + humanReadableAmount(numbers.total);
        });
        getJSON(dataURL + '/sponsors.json', function (err, sponsors) {
            const sponsorsElem = document.getElementById('sponsors');
            const privateSponsors = numbers.count - sponsors.length;
            sponsors.forEach(function (sponsor) {
                sponsorsElem.innerHTML += `
                    <a href="${sponsor.url}" class="sponsorship-item" title="@${sponsor.name}">
                        <img src="${sponsor.image}&size=72">
                    </a>
                `;
            });
            if (privateSponsors > 0) {
                sponsorsElem.innerHTML += `
                    <a href="${sponsorURL}" class="sponsorship-item private">
                        +${privateSponsors}
                    </a>
                `;
            }
        });
    });
    getJSON(dataURL + '/sponsorsBronze.json', function (err, sponsors) {
        const bronzeSponsors = document.getElementById("bronze-sponsors");
        if (sponsors) {
            let html = '';
            html += '<b>Bronze sponsors</b><p>'
            sponsors.forEach(function (sponsor) {
                html += `
                    <a href="${sponsor.url}" target="_blank" title="${sponsor.name}">
                        <img alt="${sponsor.name}" src="${sponsor.image}" style="height: ${sponsor.imageHeight}px;">
                    </a>
                `
            });
            html += '</p>'
            bronzeSponsors.innerHTML = html;
        }
    });
}
