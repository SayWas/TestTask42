document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const orgDoSelect = document.getElementById('id_organization_do');
    const orgPoSelect = document.getElementById('id_organization_po');
    let initialLoad = true;

    function createOption(value, text, isSelected) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = text;
        if (isSelected) option.selected = true;
        return option;
    }

    async function updateSelectOptions(select, users, selectedUserId) {
        const currentSelectedValue = select.value;
        const currentSelectedText = select.options[select.selectedIndex] ? select.options[select.selectedIndex].textContent : '';
        select.innerHTML = '';
        select.appendChild(createOption('', '---------', !selectedUserId));
        if (initialLoad)
            select.appendChild(createOption(currentSelectedValue, currentSelectedText, true));

        for (const user of users) {
            if (!initialLoad || currentSelectedValue != user.id) {
                const isSelected = user.id == selectedUserId;
                select.appendChild(createOption(user.id, user.text, isSelected));
            }
        }
    }

    async function fetchAndUpdateUsers() {
        const orgDoId = orgDoSelect.value;
        const orgPoId = orgPoSelect.value;

        try {
            const response = await fetch(`/api/fetch_users/?org_do_id=${orgDoId}&org_po_id=${orgPoId}`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                }
            })
            const users = await response.json();
            console.log(users, orgDoId, orgPoId);
            const allSelects = document.querySelectorAll('[id^="id_roles-"][id$="-user"]');

            for (const select of allSelects) {
                await updateSelectOptions(select, users, select.value);
            }
            initialLoad = false;
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    }

    if (orgDoSelect && orgPoSelect) {
        orgDoSelect.addEventListener('change', fetchAndUpdateUsers);
        orgPoSelect.addEventListener('change', fetchAndUpdateUsers);
        fetchAndUpdateUsers();
    }
});
