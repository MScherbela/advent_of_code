use std::fs;
use itertools::Itertools;
use std::collections::{HashSet, HashMap, VecDeque};

type NodeKey = u32;
type Edges = HashMap<NodeKey, Vec<NodeKey>>;

fn parse_input(fname: &str) -> Vec<(u32, u32)> {
    let content = fs::read_to_string(fname).expect("Cannot read input file.");
    let mut coords_list = Vec::new();
    for line in content.split("\n") {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        let coords = line.split(",").map(|x| x.parse().unwrap());
        coords_list.push(coords.collect_tuple().unwrap());
    }
    coords_list
}

fn node_key(r: u32, c: u32, n_cols: u32) -> NodeKey {
    r * n_cols + c
}

fn get_neighbours(r:u32, c: u32, n_rows: u32, n_cols: u32, walls: &HashSet<NodeKey>) -> Vec<NodeKey> {
    let mut neighbours = Vec::new();
    if r > 0 {
        neighbours.push(node_key(r-1, c, n_cols));
    }
    if r < n_rows - 1 {
        neighbours.push(node_key(r+1, c, n_cols));
    }
    if c > 0 {
        neighbours.push(node_key(r, c-1, n_cols));
    }
    if c < n_cols - 1 {
        neighbours.push(node_key(r, c+1, n_cols));
    }
    neighbours.retain(|x| !walls.contains(x));
    neighbours
}

fn build_graph(n_rows: u32, n_cols: u32, walls: &[(u32, u32)]) -> Edges {
    let walls: HashSet<NodeKey> = HashSet::from_iter(walls.iter().map(|(r,c)| node_key(*r, *c, n_cols)));
    let mut edges = HashMap::new();
    for r in 0..n_rows {
        for c in 0..n_cols {
            let node = node_key(r, c, n_cols);
            if walls.contains(&node) {
                continue;
            }
            edges.insert(node, get_neighbours(r, c, n_rows, n_cols, &walls));
        }
    }
    edges
}

fn get_distances_bfs(edges: &Edges, start: NodeKey) -> HashMap<NodeKey, u32>{
    let mut frontier = VecDeque::new();
    let mut distances = HashMap::new();
    distances.insert(start, 0);
    frontier.push_back(start);
    while !frontier.is_empty() {
        let node = frontier.pop_front().unwrap();
        let dist = *distances.get(&node).unwrap();
        for neighbour in edges.get(&node).unwrap() {
            if distances.contains_key(neighbour) {
                continue;
            }
            distances.insert(*neighbour, dist + 1);
            frontier.push_back(*neighbour);
        }
    }
    distances
}

fn can_reach_exit(walls: &[(u32, u32)], n_rows: u32, n_cols: u32) -> bool {
    let edges = build_graph(n_rows, n_cols, walls);
    let distances = get_distances_bfs(&edges, node_key(0, 0, n_cols));
    distances.contains_key(&node_key(n_rows - 1, n_cols -1, n_cols))
}

fn main() {
    // get input file name from argv
    let fname = std::env::args().nth(1).expect("No input file provided.");
    let coords_list = parse_input(&fname);
    let mut n_cols = 71;
    let mut n_rows = 71;
    let mut n_walls_part1 = 1024;
    if fname.contains("test_input") {
        n_cols = 7;
        n_rows = 7;
        n_walls_part1 = 12;
    }
    let key_start = node_key(0, 0, n_cols);
    let key_end = node_key(n_rows - 1, n_cols - 1, n_cols);

    // Truncate walls list for part 1
    let walls_part1 = &coords_list[..n_walls_part1];
    let edges_part1 = build_graph(n_rows, n_cols, walls_part1);
    let distances = get_distances_bfs(&edges_part1, key_start);
    let part1 = distances.get(&key_end).expect("No path from start to end");
    println!("Part 1: {part1}");

    // Bisection search for part 2
    let mut idx_low = 0;
    let mut idx_high = coords_list.len();
    while (idx_low + 1) != idx_high {
        let pivot = (idx_high + idx_low) / 2;
        if can_reach_exit(&coords_list[..=pivot], n_rows, n_cols) {
            idx_low = pivot;
        }
        else {
            idx_high = pivot;
        }
    }
    println!("Part 2: {:?}", coords_list[idx_high]);
}
