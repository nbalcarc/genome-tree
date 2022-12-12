use crate::structs::{PhyloTree, Genome};
use std::{path::Path, env, fs};

mod algorithms;
mod errors;
mod structs;

fn main() {
    let result = algorithms::levenshtein("kit", "glimmen");
    println!("{}", result);
    println!("{}", algorithms::levenshtein("kitten", "alderkitten"));
    println!("{}", algorithms::levenshtein("alderkitten", "kitten"));
    dbg!(algorithms::file_size("/home/terrior/Programming/genome-tree/src/test.txt"));

    //algorithms::generate_kmers(file_dir, k, num);
    //let dir = env::current_dir().unwrap().as_path().display().to_string();

    let mut tree = structs::PhyloTree::new();


    
    let dir = env::current_dir().unwrap().to_str().unwrap().to_owned(); //get the current working directory
    let paths = fs::read_dir(dir + "/genomes").unwrap(); //get all paths in the genomes directory

    // iterate through all genome folders
    for path in paths {
        //println!("Name: {}", path.unwrap().path().display());
        // iterate through all files in the genome folder
        for file in fs::read_dir(path.unwrap().path().to_str().unwrap()).unwrap() {
            //let x: String = String::from(file.unwrap().file_type().unwrap());
            
            //let file_name = file.unwrap().path().file_name().unwrap().to_str().unwrap();
            //println!("{}", file_name);

            //println!("{}", file);
            //let file_name = String::from(file.unwrap().file_name().to_str().unwrap());
            let file_path = String::from(file.unwrap().path().to_str().unwrap());
            if !&file_path.ends_with(".fna") {
                continue;
            }
            //println!("{}", file_name);
            let kmers = algorithms::generate_kmers(&file_path, 16, 20).unwrap();
            let mut genome = Genome {
                path: Vec::new(),
                dir: file_path,
                kmers: kmers,
                closest_relative: Vec::new(),
                closest_distance: 0,
            };
            //dbg!(genome);
            tree.push(genome);

        }
    }

    //algorithms::generate_kmers(dir + "/genomes/", k, num)


    let tree = PhyloTree::new();
}
