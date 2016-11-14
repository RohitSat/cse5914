CREATE TABLE IF NOT EXISTS jokes (
        id INTEGER PRIMARY KEY,
        type TEXT
);

CREATE TABLE IF NOT EXISTS joke_parts (
        id INTEGER PRIMARY KEY,
        jokeId INTEGER,
        part TEXT,
        FOREIGN KEY(jokeId) REFERENCES jokes(id)
);

INSERT INTO jokes (id, type) values (NULL, "knock knock");
INSERT INTO joke_parts(id,jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Knock knock") ;
INSERT INTO joke_parts(id,jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Canoe");
INSERT INTO joke_parts(id,jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Canoe come out and play with me today?") ;

INSERT INTO jokes (id, type) values (NULL, "knock knock");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes),"Knock, knock");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes),"Who!");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes),"That’s what an owl says!");

INSERT INTO jokes (id, type) values (NULL, "knock knock");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes), "Knock, knock");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes), "Lettuce");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes), "Lettuce in, it’s cold out here.");

INSERT INTO jokes (id, type) values (NULL, "knock knock");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes), "Knock, knock");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes), "Honey bee");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes), "Honey bee a dear and get me some juice.");


--INSERT INTO jokes (id, type) values (3, 1);
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Wooden shoe INSERT INTO joke_parts(id, jokeId, part) values(" Wooden shoe like to hear another joke?
--                
--INSERT INTO jokes (id, type) values (3, 1);
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" A broken pencil. INSERT INTO joke_parts(id, jokeId, part) values(" Oh never mind it’s pointless.
--
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Cow says. INSERT INTO joke_parts(id, jokeId, part) values(" No silly, a cow says Mooooo!
--
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Double INSERT INTO joke_parts(id, jokeId, part) values(" W
--
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Mikey INSERT INTO joke_parts(id, jokeId, part) values(" Mikey doesn’t fit in the keyhole!
--
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Atch INSERT INTO joke_parts(id, jokeId, part) values(" Bless you!
--
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" I am INSERT INTO joke_parts(id, jokeId, part) values(" You don’t know who you are?
--
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Ya. INSERT INTO joke_parts(id, jokeId, part) values(" Wow, I’m excited to see you too.
--
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Figs. INSERT INTO joke_parts(id, jokeId, part) values(" Figs the doorbell, it’s broken!
--
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Boo! INSERT INTO joke_parts(id, jokeId, part) values(" Don’t cry, it’s just me.
--
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Who’s there?INSERT INTO joke_parts(id, jokeId, part) values(" Iva. INSERT INTO joke_parts(id, jokeId, part) values(" Iva who? INSERT INTO joke_parts(id, jokeId, part) values(" I’ve a sore hand from knocking!
--
-- INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Who’s there?INSERT INTO joke_parts(id, jokeId, part) values(" Avenue. INSERT INTO joke_parts(id, jokeId, part) values(" Avenue who? INSERT INTO joke_parts(id, jokeId, part) values(" Avenue knocked on this door before?
--                    
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Who’s there?INSERT INTO joke_parts(id, jokeId, part) values(" A little old lady. INSERT INTO joke_parts(id, jokeId, part) values(" A little old lady who? INSERT INTO joke_parts(id, jokeId, part) values(" I didn’t know you could yodel.
--
--INSERT INTO joke_parts(id, jokeId, part) values( Knock, knock.INSERT INTO joke_parts(id, jokeId, part) values(" Who’s there? INSERT INTO joke_parts(id, jokeId, part) values(" Banana. INSERT INTO joke_parts(id, jokeId, part) values(" Banana who? INSERT INTO joke_parts(id, jokeId, part) values(" Knock, knock. INSERT INTO joke_parts(id, jokeId, part) values(" Who’s there? INSERT INTO joke_parts(id, jokeId, part) values(" Banana. INSERT INTO joke_parts(id, jokeId, part) values(" Banana who? INSERT INTO joke_parts(id, jokeId, part) values(" Knock, knock. INSERT INTO joke_parts(id, jokeId, part) values(" Who’s there? INSERT INTO joke_parts(id, jokeId, part) values(" Banana. INSERT INTO joke_parts(id, jokeId, part) values(" Banana who? INSERT INTO joke_parts(id, jokeId, part) values(" Knock, knock. INSERT INTO joke_parts(id, jokeId, part) values(" Who’s there? INSERT INTO joke_parts(id, jokeId, part) values(" Orange. INSERT INTO joke_parts(id, jokeId, part) values(" Orange who? INSERT INTO joke_parts(id, jokeId, part) values(" Orange you glad I didn’t say banana?
--

-- question jokes
INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "What happens to a frogs car when it breaks down?");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "It gets toad away");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Why was six scared of seven?");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Because seven ate nine. ");
        
INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Can a kangaroo jump higher than the Empire State Building?");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Of course. The Empire State Building can not jump");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Did you hear about the kidnapping at school?") ;
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), " Its okay. He woke up.");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Why does Humpty Dumpty love autumn?");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), " Because Humpty Dumpty had a great fall");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Why did the witches team lose the baseball game?");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), " Their bats flew away.");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "What do you call a pig that does karate?");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), " A pork chop.");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Whats the difference between Windows 95 and a virus");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), " A virus does something");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Why are bananas never lonely?");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), " Because they hang around in bunches");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "What does a baby computer call his father");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Data");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "What is a ghost-proof bicycle");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes), " One with no spooks in it");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "Where did the kittens go on their class trip");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes), " To a mewseum");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "What do you call cattle with a sense of  humor");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes), " Laughing stock");

INSERT INTO jokes (id, type) values (NULL, "question");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "What did the farmer call the cow that would not give him any milk");
INSERT INTO joke_parts(id, jokeId, part) values(NULL, (SELECT MAX(id) from jokes), " An udder failure");

-- one liners
INSERT INTO jokes (id, type) values (NULL, "oneliner");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes),"A man got hit in the head with a can of Coke, but he was alright because it was a soft drink");

INSERT INTO jokes (id, type) values (NULL, "oneliner");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "I was wondering why the ball kept getting bigger and bigger, and then it hit me");

INSERT INTO jokes (id, type) values (NULL, "oneliner");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes),"Zoo Keeper: I have lost one of my elephants. Other Zoo Keeper: why don't you put an advert in the paper. Zoo keeper: Don't be silly he can't read ");

INSERT INTO jokes (id, type) values (NULL, "oneliner");
INSERT INTO joke_parts(id, jokeId, part) values (NULL, (SELECT MAX(id) from jokes), "camper: Look at that bunch of cows. Farmer: Not  bunch, herd. Camper: Heard what? Farmer: Of cows. Camper: Sure  I have heard of cows. Farmer: No, I mean a cowherd. Camper: So  what? I have no secrets from cows!");
