#PROJECT IS NOW IN: STUDY VERSION

## NgramGraph Dependencies:

# Install pip
sudo apt-get install python-pip


# Install python graph library "Networkx"
sudo pip install networkx


# Install MathPlot lib
sudo apt-get install python-dev
sudo apt-get install python-tk
sudo python -m pip install matplotlib

# Install Pydot, PydotPlus
sudo pip install pydot
sudo pip install pydotplus

# Install python graph viz library "pygraphviz"
sudo apt-get install graphviz libgraphviz-dev pkg-config
sudo pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/"
