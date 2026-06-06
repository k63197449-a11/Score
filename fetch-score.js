const fs = require('fs');
const axios = require('axios');

const API_URL = 'https://cricket-api-unoffical.vercel.app/live';

async function getLiveScore() {
    try {
        console.log('Fetching live scores...');
        const response = await axios.get(API_URL);
        
        if (response.data && response.data.matches && response.data.matches.length > 0) {
            const liveMatch = response.data.matches[0]; 
            
            const matchName = liveMatch.title || "Live Match";
            const team1 = liveMatch.team1 || "Team 1";
            const team2 = liveMatch.team2 || "Team 2";
            const score1 = liveMatch.team1Score || "0/0";
            const score2 = liveMatch.team2Score || "0/0";
            const status = liveMatch.status || "Match in progress";

            const finalScoreText = `🎯 ${matchName}\n🏏 ${team1}: ${score1} vs ${team2}: ${score2}\n📢 Status: ${status}`;
            
            fs.writeFileSync('score.txt', finalScoreText);
            console.log('Score updated successfully!');
        } else {
            fs.writeFileSync('score.txt', 'No Live Match Available Right Now.');
        }
    } catch (error) {
        fs.writeFileSync('score.txt', '🔄 Refreshing Live Score...');
    }
}

getLiveScore();
