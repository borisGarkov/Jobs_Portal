standard_packages_btn = document.getElementById('standard_packages');
personalised_packages_btn = document.getElementById('personalised_packages');
standard_packages_section = document.getElementById('standard_packages_section');
personalised_packages_section = document.getElementById('personalised_packages_section');

standard_packages_btn.addEventListener('click', onClickStandard);
personalised_packages_btn.addEventListener('click', onClickPersonalised);

function onClickStandard(e) {
    standard_packages_btn.className = 'btn_packages_active';
    personalised_packages_btn.className = 'btn_packages_inactive';
    setTimeout(() => {
        personalised_packages_section.style.display = 'none';
        personalised_packages_section.style.opacity = '0';
        standard_packages_section.style.display = 'block';
        standard_packages_section.style.opacity = '1';
    }, 200);
};

function onClickPersonalised(e) {
    standard_packages_btn.className = 'btn_packages_inactive';
    personalised_packages_btn.className = 'btn_packages_active';
    setTimeout(() => {
        standard_packages_section.style.display = 'none';
        standard_packages_section.style.opacity = '0';
        personalised_packages_section.style.display = 'block';
        personalised_packages_section.style.opacity = '1';
    }, 200);
};