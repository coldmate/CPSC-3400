/// Alen Ovalles
/// hw5.fs
/// 02-21-2024

/// findFirstInt 
/// parameters: a list of tuples of var
/// return: the int bound of var
let rec findFirstInt varStr = function 
    | [] -> 0
    | hd :: tl when fst(hd) = varStr -> 
        snd(hd) 
    | hd :: tl -> 
        findFirstInt varStr tl

/// eval
/// parameters: a list of tuples, an equation as a str in postfix notation
/// return: a int list with only one element, the solution to the given equation
let eval vars (expr:string) = 
    let strSeq = Seq.toList expr |> Seq.map(fun x -> string x)  
    let strList = Seq.toList strSeq                            

    let rec innerEval vars stack strList =
        match strList with
        | [] -> stack
        | hd :: tl when hd = "+" -> 
            let num1::num2::rest = stack 
            innerEval vars ((num1 + num2)::rest) tl
        | hd :: tl when hd = "-" -> 
            let num1::num2::rest = stack 
            innerEval vars ((num2 - num1)::rest) tl
        | hd :: tl when hd = "*" ->
            let num1::num2::rest = stack 
            innerEval vars ((num1 * num2)::rest) tl
        | hd :: tl when hd = "/" -> 
            let num1::num2::rest = stack 
            innerEval vars ((num2 / num1)::rest) tl
        | hd :: tl when hd = "$" -> 
            let num1::num2::rest = stack 
            innerEval vars (num2::num1::rest) tl
        | hd :: tl when hd = "@" -> 
            let char1::char2::restOfChars = strList
            let newInt::rest = stack
            innerEval ((char2, newInt)::vars) rest restOfChars
        | hd :: tl when hd = " " -> 
            innerEval vars stack tl
        | hd :: tl -> 
            innerEval vars ((findFirstInt hd vars)::stack) tl

    innerEval vars [] strList