## static files

when trying to load a static file like, image, js, css, add the `load statice`

```html
<head>
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<title>Document</title>
	{% load static %}
	<link rel="stylesheet" href="{% static 'css/main.css' %}" />
</head>
```

## form

For current form, add the method to the `<form>` and `name` attribute to each input field.

```html
<form method="POST" id="form">
	<div class="form-control">
		<label for="text">Description</label>
		<input
			type="text"
			name="description"
			id="text"
			placeholder="Enter description..." />
	</div>
	<div class="form-control">
		<label for="amount"
			>Amount <br />
			<small>(-100 = expense, 100 = income)</small></label
		>
		<input
			type="number"
			name="amount"
			id="amount"
			placeholder="Enter amount..." />
	</div>
	<button class="btn">Add transaction</button>
</form>
```

When we don't specify the `action` attribute in a `<form>` tag, the form submits the data to the current URL (the URL of the page where the form is rendered).

### Behavior without action:

If the form is rendered at `http://example.com/expenses`, the data will be submitted to `http://example.com/expenses` when the user submits the form.
In this case, the server should have a route that handles the form submission at the same URL.
we get access to the submitted data through `request`.

### Crucial

For comparison operator inside a template, always keep a space between the operator and the operand
wrong!!!

```sh
transaction.expense_type =='DEBIT'
```

correct

```sh
transaction.expense_type == 'DEBIT'
```

```html
<i>
	class="{% if transaction.expense_type == 'DEBIT' %} minus {% else %} plus {%
	endif %}"></i
>
```
