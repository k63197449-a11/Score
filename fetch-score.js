const fs = require('fs');
const axios = require('axios');

const API_URL = 'https://cricket-api-unoffical.vercel.app/live';

async function getLiveScore() {
    try {
        console.log('Fetching live scores...');
        const response = await axios.get(API_URL);
        
        if (response.data && response.data.matches && response.data.matches.length > 0) {
            const liveMatch = response.data.matches[0]; 
            
            const matchName = liveMatch.title || "লাইভ ম্যাচ";
            const team1 = liveMatch.team1 || "প্রথম দল";
            const team2 = liveMatch.team2 || "দ্বিতীয় দল";
            const score1 = liveMatch.team1Score || "০ রান";
            const score2 = liveMatch.team2Score || "০ রান";
            const status = liveMatch.status || "খেলা চলছে";

            // এআই ভয়েস যেন সুন্দর করে বাংলায় রিড করতে পারে তার ফরম্যাট
            const finalScoreText = `সুপ্রিয় দর্শক, খেলায় আপনাকে স্বাগতম। বর্তমানে চলছে, ${matchName}। ${team1} এর বর্তমান স্কোর ${score1}। অপরদিকে ${team2} এর স্কোর ${score2}। সর্বশেষ আপডেট অনুযায়ী, ${status}।`;
            
            fs.writeFileSync('score.txt', finalScoreText);
            console.log('Voice Text Generated!');
        } else {
            fs.writeFileSync('score.txt', 'এই মুহূর্তে কোনো ম্যাচ লাইভ নেই। পরবর্তী আপডেটের জন্য আমাদের সাথেই থাকুন। ধন্যবাদ।');
        }
    } catch (error) {
        fs.writeFileSync('score.txt', 'লাইভ স্কোর আপডেট করা হচ্ছে। দয়া করে একটু অপেক্ষা করুন।');
    }
}

getLiveScore();
