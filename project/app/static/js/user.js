const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
    email: {
        type: String,
        required: true,
        unique: true,
        trim: true,
        match: [/^\S+@\S+\.\S+$/, 'Invalid email format'], // ✅ Email validation
    },
    password: {
        type: String,
        required: true,
        minlength: 6, // ✅ Minimum password length
    },
    role: {
        type: String,
        enum: ['student', 'parent', 'institute'],
        required: true,
        default: 'student', // ✅ Default role assignment
    },
}, { timestamps: true }); // ✅ Automatically adds createdAt & updatedAt timestamps

// ✅ Hash password before saving to database
userSchema.pre('save', async function (next) {
    if (!this.isModified('password')) return next(); // Avoid re-hashing if password hasn't changed
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
});

// ✅ Method to validate password during login
userSchema.methods.comparePassword = async function (password) {
    return await bcrypt.compare(password, this.password);
};

// ✅ Remove password field when returning user data
userSchema.methods.toJSON = function () {
    const user = this.toObject();
    delete user.password;
    return user;
};

const User = mongoose.model('User', userSchema);
module.exports = User;
