# Pricing Options Using Monte Carlo Methods

This Python-based Monte Carlo library for calculating option prices is based on the first 5 chapters of the classic finance book ["C++ Design Patterns and Derivatives Pricing" by Mark S. Joshi][1].

The first iteration of this library is implemented using the Python Standard Library. I am planning to extend it to cover NumPy and Cython shortly.

### Getting Started

Install prerequisites:
```
$ conda env create -f environment.yml 
```

Run unit tests:
```
$ python -m unittest discover src
```

Run Jupyter notebook containing usage examples:
```
jupyter notebook notebooks/MonteCarlo.ipynb 
```

### Potential Future Improvements

* NumPy implementation
* Cython implementation

### References

* https://web.archive.org/web/20190107102714/http://markjoshi.com/design
* https://web.archive.org/web/20160817064828if_/http://markjoshi.com/design/ClassDiagram.jpg

[1]: https://www.amazon.com/Patterns-Derivatives-Pricing-Mathematics-Finance/dp/0521721628
