from django import forms
from django.utils.safestring import mark_safe

class BaseForm(forms.Form):
    def as_floating(self):
        """
        Returns:
            SafeString: Bootstrap 5 floating label form fields.
        See Also:
            https://getbootstrap.jp/docs/5.3/forms/floating-labels/
        """
        output = '<div class="d-grid gap-3">'
        for field in self:
            classList = set(field.field.widget.attrs.get('class', '').split())
            classList.add('form-control')
            if field.errors:
                classList.add('is-invalid')

            field.field.widget.attrs.update({
                'class': ' '.join(classList),
                'placeholder': field.label,
            })

            # HTMLを生成
            output += '<div class="form-floating">'

            output += f'{field}'
            output += f'{field.label_tag(label_suffix="")}'

            if field.help_text:
                output += f'<div class="form-text"><small>{field.help_text}</small></div>'

            if field.errors:
                output += f'<div class="invalid-feedback">{field.errors}</div>'

            output += '</div>'

        output += '</div>'
        return mark_safe(output)

    def as_controls(self):
        """
        Returns:
            SafeString: Bootstrap 5 form fields.
        See Also:
            https://getbootstrap.jp/docs/5.3/forms/form-control/
        """
        output = '<div class="d-grid gap-3">\n'
        for field in self:
            classList = set(field.field.widget.attrs.get('class', '').split())
            classList.add('form-control')
            if field.errors:
                classList.add('is-invalid')

            field.field.widget.attrs.update({
                'class': ' '.join(classList),
            })

            # HTMLを生成
            output += '<div>'

            output += f'{field.label_tag(attrs={"class": "form-label ms-1 mb-1"}, label_suffix="")}'
            output += f'{field}'

            if field.help_text:
                output += f'<div class="form-text"><small>{field.help_text}</small></div>'

            if field.errors:
                output += f'<div class="invalid-feedback">{field.errors}</div>'

            output += '</div>\n'

        output += '</div>\n'

        return mark_safe(output)
