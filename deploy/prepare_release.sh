# Run the examples to catch public API changes.
read -p "What version is being released? " version

if ! grep -q $version "pyshgp/__init__.py"; then
  echo "That is not the version in pyshgp/__init__.py. Please correct."
  exit
fi

source deploy/deploy_setup.sh


# Run the examples to catch public API changes.
read -p "Would you like to run all examples? " yesno

if [ "$yesno" == "y" ]; then
    source deploy/run_examples.sh
fi


# Check for style issues
read -p "Would you like to run flake8 linter for style issues? " yesno

if [ "$yesno" == "y" ]; then
    python3 -m flake8 pyshgp/
    python3 -m flake8 examples/
fi


# Build Documenation
read -p "Have you written the release notes in the documentation? " yesno

if [ ! "$yesno" == "y" ]; then
    echo "Please write release notes documentation before proceeding."
    exit
fi

pushd docs_source
make api
make
popd

read -p "Would you like to push the documentation to GitHub? (Uses current branch) " yesno

if [ "$yesno" == "y" ]; then
    git add docs_source/
    git add docs/
    git commit -m "Update documentation site for next release."
    git push
fi


# Build the Wheel
python3 setup.py sdist bdist_wheel

deactivate

cat << EOF

REMAINING TO-DOS BEFORE RELEASE IS FINAL
========================================
- Merge in any relevant outstanding Pull Requests to master.
- Create a new release on GitHub.
- Publish the wheel with "python3 -m twine upload".
EOF
