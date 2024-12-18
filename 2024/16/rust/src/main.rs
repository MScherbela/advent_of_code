use std::{collections::HashMap, collections::BinaryHeap, fs};

type Grid = Vec<Vec<bool>>;
type Direction = isize;
const COST_MOVE: usize = 1;
const COST_TURN: usize = 1000;

const DIRECTIONS: [(isize, isize);4] = [(0, 1), (-1, 0,), (0, -1), (1, 0)];

#[derive(Clone, Debug)]
struct Pos {
    r: isize,
    c: isize,
}

#[derive(Debug)]
struct Node {
    pos: Pos,
    dir: Direction,
}

impl Pos {
    fn equals(&self, other: &Pos) -> bool {
        (self.r == other.r) && (self.c == other.c)
    }
} 

fn parse_input(fname: &str) -> (Grid, Pos, Pos) {
    let mut grid: Grid = Vec::new();
    let mut start = Pos { r: 0, c: 0 };
    let mut end = Pos { r: 0, c: 0 };

    let contents = fs::read_to_string(fname)
        .expect("Cannot read input file");
    let lines = contents.split("\n");
    for (r, line) in lines.enumerate() {
        grid.push(Vec::new());
        for (c, ch) in line.chars().enumerate() {
            if ch == 'S' {
                start = Pos { r: r as isize, c: c as isize};
                grid[r].push(true);
            } 
            else if ch == 'E' 
            {
                end = Pos { r: r as isize, c: c as isize};
                grid[r].push(true);
            } else if ch == '.' {
                grid[r].push(true);
            }
            else {
                grid[r].push(false);
            }
        }
    }
    (grid, start, end)
}

fn build_graph(grid: &Grid) -> (Vec<Node>, Vec<Vec<(usize, usize)>>) {
    let mut nodes = Vec::new();
    let mut node_lookup = HashMap::new();
    let n_cols: isize = grid[0].len() as isize;
    const N_DIRS: isize = 4;

    let lookup_key = |r: isize, c: isize, dir: isize| -> isize {N_DIRS * (r * n_cols + c) + dir};

    // Step 1: build a Vec of all nodes and a lookup dict to map (pos, dir) => node
    let mut node_index: usize = 0;
    for (r, row) in grid.iter().enumerate() {
        let r = r as isize;
        for (c, is_path) in row.iter().enumerate() {
            if !is_path {
                continue;
            }
            let c = c as isize;
            for dir in 0..4 {
                let node = Node { pos: Pos {r, c}, dir };
                node_lookup.insert(lookup_key(r, c, dir), node_index);
                nodes.push(node);
                node_index += 1;
            }
        }
    }

    let mut edges = Vec::new();
    for node in nodes.iter() {
        let (r, c, dir) = (node.pos.r, node.pos.c, node.dir);
        let mut outbound_edges = Vec::new(); 
        
        // Move to neighbour
        let (dr, dc) = DIRECTIONS[dir as usize];
        let neighbour_key = lookup_key(r + dr, c + dc, dir);
        let neighbour_idx = node_lookup.get(&neighbour_key);
        if neighbour_idx.is_some() {
            outbound_edges.push((COST_MOVE, *neighbour_idx.unwrap()));
        }

        let neighbour_idx_left = *node_lookup.get(&lookup_key(r,c, (dir + 1)%4)).unwrap();
        let neighbour_idx_right = *node_lookup.get(&lookup_key(r,c, (dir + 3) % 4)).unwrap();
        outbound_edges.push((COST_TURN, neighbour_idx_left));
        outbound_edges.push((COST_TURN, neighbour_idx_right));
        edges.push(outbound_edges);
    }
    (nodes, edges)
}

fn get_shortest_distances(nodes: &Vec<Node>, edges: &Vec<Vec<(usize, usize)>>, start_idx: usize) -> (Vec<usize>, Vec<Vec<usize>>) {
    let mut distances = vec![usize::MAX; nodes.len()];
    let mut predecessors = vec![Vec::new(); nodes.len()];

    distances[start_idx] = 0;
    let mut frontier = BinaryHeap::new();
    frontier.push((0, start_idx));
    // let mut frontier = Vec::new();
    // frontier.push(start_idx);

    while frontier.len() > 0 {
        let (_, idx) = frontier.pop().unwrap();
        let current_dist = distances[idx];
        for (edge_dist, neighbour_idx) in edges[idx].iter() {
            let new_dist = current_dist + edge_dist;
            if new_dist < distances[*neighbour_idx] {
                distances[*neighbour_idx] = new_dist;
                predecessors[*neighbour_idx].clear();
                frontier.push((-(new_dist as isize), *neighbour_idx));
            }
            if new_dist == distances[*neighbour_idx] {
                predecessors[*neighbour_idx].push(idx);
            }
        }
    }
    (distances, predecessors)
}

fn main() {
    let (grid, start_pos, end_pos) = parse_input("input.txt");
    let (nodes, edges) = build_graph(&grid);

    let mut idx_start = 0;
    let mut idx_end = Vec::new();
    for (idx, node) in nodes.iter().enumerate() {
        if (node.dir == 0) && node.pos.equals(&start_pos) {
            idx_start = idx;
        }
        if node.pos.equals(&end_pos) {
            idx_end.push(idx);
        }
    }

    let (distances, _predecessors) = get_shortest_distances(&nodes, &edges, idx_start);
    let end_distance = idx_end.iter().map(|idx| distances[*idx]).min().unwrap();
    for idx in idx_end.iter(){
        println!("{}", distances[*idx]);
    }
    println!("Shortest distance to end: {end_distance}");

}
