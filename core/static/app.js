// Nav toggler for mobile
const navToggler = document.querySelector('.nav-menu-toggler');
const layoutBody = document.querySelector('.layout-body');
navToggler.addEventListener('click', () => {
    layoutBody.classList.toggle('nav-expanded');
});

(async () => {
    const mediaQuery = window.matchMedia('(min-width: 600px)');
    const handleMediaQuery = (e) => {
        navToggler.disabled = !!e.matches;
    };

    mediaQuery.addEventListener('change', handleMediaQuery);
    handleMediaQuery(mediaQuery);
})();


// Dropdown
const dropdownItems = document.querySelectorAll('[data-dropdown="dropdown"]');
dropdownItems.forEach((parent) => {
    const trigger = document.querySelector('[data-dropdown="trigger"]');
    const target = document.querySelector('[data-dropdown="target"]');

    const targetItems = target.querySelectorAll('button, a');
    for (let i = 0; i < targetItems.length; i++) {
        const item = targetItems[i];
        const nextItem = i < targetItems.length ? targetItems[i + 1] : null;
        const prevItem = i >= 0 ? targetItems[i - 1] : null;
        item.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (nextItem) {
                    nextItem.focus();
                }
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (prevItem) {
                    prevItem.focus();
                }
            } else if (e.key === 'Escape') {
                e.preventDefault();
                parent.classList.remove('is-open');
                trigger.focus();
            }
        });
    }

    trigger.addEventListener('click', () => {
        parent.classList.toggle('is-open');
        target.querySelector('button, a').focus();
    });
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('[data-dropdown="dropdown"]')) {
        dropdownItems.forEach((parent) => {
            parent.classList.remove('is-open');
        });
    }
});

// Popovers
(async () => {
    // <div class="popover"><button class="popover-trigger custom-class">Hover me</button><span class="popover-label">Popover Label!!!</span></div>
    const popovers = document.querySelectorAll('.bb-popover');

    popovers.forEach((popover) => {
        const trigger = popover.querySelector('.popover-trigger');
        const label = popover.querySelector('.popover-label');

        if (!trigger || !label) {
            return;
        }

        trigger.addEventListener('mouseenter', () => {
            label.classList.add('is-visible');
        });

        trigger.addEventListener('mouseleave', () => {
            label.classList.remove('is-visible');
        });
    });
})();

// Open modal (be-open class)
(async () => {
    const element = document.querySelector('.be-open');
    if (element) {
        new bootstrap.Modal(element).show();

        element.classList.remove('be-open');
        if (element.classList.contains('be-fade')) {
            element.classList.add('fade');
            element.classList.remove('be-fade');
        }

    }
})();

// Close modal (be-close class)
(async () => {
    const element = document.querySelector('.be-close');
    if (element) {
        const bsModal = new bootstrap.Modal(element);

        bsModal.show()
        if (element.classList.contains('be-fade')) {
            element.classList.add('fade');
            element.classList.remove('be-fade');
        }

        setTimeout(() => {
            bsModal.hide();
        }, 100);
    }
})();
