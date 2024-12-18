
use std::fs;

#[derive(Clone, Debug)]
struct Registers {
    a: usize,
    b: usize,
    c: usize,
}

enum StepOutput {
    None,
    Value(usize),
}

fn parse_input(fname: &str) -> (Registers, Vec<usize>) {
    let contents = fs::read_to_string(fname).expect("Something went wrong reading the file");

    let mut registers = Registers{ a: 0, b: 0, c: 0};
    let mut program: Vec<usize> = Vec::new();

    for line in contents.lines() {
        let line = line.trim();
        if line.starts_with("Register A:") {
            registers.a = line.split(": ").last().unwrap().parse().unwrap();
        } else if line.starts_with("Register B:") {
            registers.b = line.split(": ").last().unwrap().parse().unwrap();
        } else if line.starts_with("Register C:") {
            registers.c = line.split(": ").last().unwrap().parse().unwrap();
        } else if line.starts_with("Program:"){
            let values = line.split(": ").last().unwrap().split(",");
            program = values.map(|x| x.trim().parse().unwrap()).collect();
        }
    }
    (registers, program)
}

fn get_combo_operand(reg: &Registers, value: usize) -> usize {
    if value <= 3 {
        value
    }
    else {
        match value {
            4 => reg.a,
            5 => reg.b,
            6 => reg.c,
            _ => panic!("Invalid value")
        }
    }
}

fn step(reg: &mut Registers, program: &[usize], mut pos: usize) -> (usize, StepOutput) {
    let op = program[pos];
    let value_literal = program[pos+1];
    let value_combo = get_combo_operand(reg, value_literal);
    let mut output = StepOutput::None;
    match op {
        0 => {
            reg.a >>= value_combo;
            pos += 2;
        },
        1 => {
            reg.b ^= value_literal;
            pos += 2;

        },
        2 => {
            reg.b = value_combo % 8;
            pos += 2;

        },
        3 => {
            if reg.a != 0 {
                pos = value_literal;
            }
            else {
                pos += 2;
            }
        },
        4 => {
            reg.b ^= reg.c;
            pos += 2;

        }
        5 => {
            output = StepOutput::Value(value_combo % 8);
            pos += 2;

        }
        6 => {
            reg.b = reg.a >> value_combo;
            pos += 2;

        }
        7 => {
            reg.c = reg.a >> value_combo;
            pos += 2;

        }
        _ => panic!("Invalid op code {op}")
    }
    (pos, output)
}

fn simulate_program(registers: &Registers, program: &[usize]) -> Vec<usize> {
    let mut registers = registers.clone();
    let mut outputs: Vec<usize> = Vec::new();
    let mut pos = 0;
    while pos <= program.len() - 2 {
        let result = step(&mut registers, program, pos);
        pos = result.0;
        match result.1 {
            StepOutput::None => (),
            StepOutput::Value(v) => outputs.push(v),
        }
    }
    outputs
}

fn numbers_to_string(program: &[usize]) -> String {
    program.iter().map(|x| x.to_string()).collect::<Vec<String>>().join(",")
}

fn can_match_target(prefix: usize, targets: &[usize], precomputed_outputs: &[usize]) -> Result<usize, usize> {
    for i in 0..8 {
        let a = (prefix << 3) + i;
        let a_10bit = a % 1024;
        if precomputed_outputs[a_10bit] != targets[targets.len() - 1] {
            continue;
        }
        if targets.len() == 1 {
            return Ok(a);
        }
        match can_match_target((prefix << 3) + i, &targets[..targets.len()-1], precomputed_outputs) {
            Ok(v) => return Ok(v),
            Err(_) => continue,
        }
    }
    Err(0)
}


fn main() {
    // get fname from argv
    let argv = std::env::args().collect::<Vec<String>>();
    if argv.len() != 2 {
        panic!("Must provide exactly one argument, being the input file name.")
    }	
    let fname = &argv[1];

    let (mut registers, program) = parse_input(fname);
    println!("Registers: {:?}", registers);
    println!("Program: {}", numbers_to_string(&program));

    let outputs = simulate_program(&registers, &program);
    let output_string = numbers_to_string(&outputs);
    println!("Part 1: {output_string}");


    // Part 2 => this is input-specific; Assumes that the entire state required to get the next output is the last 10bits of A
    // Part2a => pre-compute possible values of a that yield a given first output value
    let mut precomputed_results = Vec::new();
    for a in 0..1024 {
        registers.a = a;
        precomputed_results.push(simulate_program(&registers, &program)[0]);
    }

    let part2 = can_match_target(0, &program, &precomputed_results).unwrap();
    println!("Part 2: {part2}");

    // Verify
    registers.a = part2;
    let outputs = simulate_program(&registers, &program);
    for (x1, x2) in outputs.iter().zip(program.iter()) {
        if x1 != x2 {
            panic!("Mismatch: {x1} != {x2}");
        }
    }
    println!("Output matches program!");
}