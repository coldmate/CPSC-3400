/// Alen Ovalles
/// CPSC 3400
/// pa4.fs
/// 02-09-2024

/// maxCubeVolume 
/// parameters: a list of tuples containing three floats
/// returns: the max volume in the list of tuples 
let rec maxCubeVolume listTuples =
    match listTuples with
    | [] -> 0.0
    | (length, width, height) :: tl ->
        let currVolume = length * width * height
        let nextVolume = maxCubeVolume tl

        if currVolume > nextVolume
            then currVolume
        else
            nextVolume


/// findMatches
/// parameters: a target str and a list of tuples, a strVal and intVal in each tuple
/// returns: a sorted list of ints based on the int corresponding to the target str 
///              if found each tuple
let rec findMatches value = function
    | [] -> []
    | (strVal, intVal) :: tl -> 
        if value = strVal
            then List.sort(intVal :: findMatches value tl)
        else
            findMatches value tl : int list
/// BST definition 
type BST = 
    | Empty
    | TreeNode of int * BST * BST

/// insert
/// parameters: an int value and an BST
/// returns: BST with added value 
let rec insert newVal tree =
    match tree with
    | Empty -> TreeNode(newVal, Empty, Empty)
    | TreeNode(value, left, right) -> 
        if newVal = value
            then tree
        elif newVal < value
            then TreeNode(value, (insert newVal left), right)
        else
            TreeNode(value, left, (insert newVal right))

/// contains
/// parameters: an target int and an BST
/// returns: a bool, if target int in tree then true else false
let rec contains target tree = 
    match tree with
    | Empty -> false
    | TreeNode(value, left, right) ->
        if target = value   
            then true
        elif target < value 
            then contains target left
        else
            contains target right
            
/// count
/// parameters: an bool func with one parameter and an BST 
/// returns: an int, the number of nodes that are true based on the bool func
let count func tree = 
    let rec loop total = function
        | Empty -> 0
        | TreeNode(value, left, right) ->
            if func value 
                then 1 + (loop total left) + (loop total right)
            else
                (loop total left) + (loop total right)
    loop 0 tree

/// evenCount
/// parameter: an BST 
/// returns: an int, the total of even numbers in tree
let evenCount tree = 
    count(fun x -> x % 2 = 0) tree
