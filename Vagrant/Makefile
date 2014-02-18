base-box:
	cd BaseBox
	vagrant package --base

release:
	@echo "Building release zipfile"
	@rm -rf rmqid-vagrant rmqid-vagrant.zip
	@cp -r Release rmqid-vagrant
	@rm -rf rmqid-vagrant/.vagrant
	@find . -name ".git" -type f|xargs rm -f
	@find . -name ".gitignore" -type f|xargs rm -f
	@find . -name ".DS_Store" -type f|xargs rm -f
	@zip -9 -r rmqid-vagrant.zip rmqid-vagrant/*
	@rm -rf rmqid-vagrant
	@echo "Done"
