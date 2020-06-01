
# Generate HTML
```
make html

sphinx-build -M html "source" "../docs"
```

# Generate API Docs
```
sphinx-apidoc -f -o source/api/ .. ../tests/ ../examples/ ../dev* ../scratch* ../setup* ../pyshgp_cli*
```
