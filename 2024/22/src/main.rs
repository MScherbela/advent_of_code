use std::collections::HashMap;
type PriceSeq = (i32, i32, i32, i32);


fn parse_input(fname: &str) -> Vec<u64> {
    let content = std::fs::read_to_string(fname).expect("Input file not found");
    content.split('\n').map(|s|s.trim().parse().unwrap()).collect()
}

fn rng_step(x: u64) -> u64 {
    const LOWER24BITS: u64 = 0xFFFFFF;
    let x = (x ^ (x << 6)) & LOWER24BITS; // mix x with x*64
    let x = (x ^ (x >> 5)) & LOWER24BITS; // mix x with x/32
    (x ^ (x << 11)) & LOWER24BITS // mix x with x*2048
}

fn rng_steps(x: u64, n_steps: usize) -> u64 {
    let mut x = x;
    for _ in 0..n_steps {
        x = rng_step(x);
    }
    x
}

fn main() {
    // Parse input
    let n_steps = 2000;
    let fname = std::env::args().nth(1).expect("No input filename provided");
    let seeds = parse_input(&fname);

    // Part 1: compute sum of iterated rng values
    let values_part1 = seeds.iter().map(|x| rng_steps(*x, n_steps));
    let part1 = values_part1.sum::<u64>();
    println!("Part 1: {part1}");

    // Part 2
    let mut seq_to_price: HashMap<PriceSeq, (u64, i32)> = HashMap::new();
    for seed in seeds {
        let mut prices = Vec::new();
        let mut x = seed;
        for _ in 0..n_steps {
            x = rng_step(x);
            prices.push((x % 10) as i32);
        }

        let price_deltas: Vec<i32> = prices.windows(2).map(|w| w[1] - w[0]).collect();

        for i in 4..n_steps {
            let seq = (price_deltas[i-4], price_deltas[i-3], price_deltas[i-2], price_deltas[i-1]);
            if !seq_to_price.contains_key(&seq) {
                seq_to_price.insert(seq, (seed, prices[i]));
            }
            else {
                let (seed_last, price_last) = seq_to_price[&seq];
                if seed_last != seed {
                    seq_to_price.insert(seq, (seed, price_last + prices[i]));
                }
            }
        }
    }

    let part2 = seq_to_price.values().map(|x| x.1).max().unwrap();
    println!("Part 2: {part2}");
}
