## Interesting Problem Solutions

### Odd

```


```


## Computational Timings

### STRING

#### With concurrent

Average Evaluation Timing of Generation: 1.59
Average Selection/Variations Timing of Generation: 0.53

#### Without Concurrent

Average Evaluation Timing of Generation: 0.974
Average Selection/Variations Timing of Generation: 0.389


### INTEGER REGRESSION (50 test cases)

#### With concurrent

Average Evaluation Timing of Generation: 2.396
Average Selection/Variations Timing of Generation: 1.681

#### Without Concurrent

Average Evaluation Timing of Generation: 4.681
Average Selection/Variations Timing of Generation: 1.563


### RSWN

#### With concurrent

Average Evaluation Timing of Generation: 17.376
Average Selection/Variations Timing of Generation: 3.265

#### Without concurrent

Average Evaluation Timing of Generation: 31.837
Average Selection/Variations Timing of Generation: 3.575

#### Solutions

Clojush found following solution at generation 45
`(\space in1 \newline string_replacechar print_string \space in1 string_removechar char_allfromstring char_stackdepth)`