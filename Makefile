format:
	fd -e bean -x bean-format -i {}

prices:
	python prices.py

commit:
	git commit -m "$(date +'%Y-%m-%d %H:%M:%S')"
